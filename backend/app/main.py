"""FastAPI entrypoint: health check, chat WebSocket, and static SPA serving.

Run with ``uvicorn backend.app.main:app``. Importing this module does not load a
settings file or connect to Bluetooth; both happen lazily on first chat use.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

from .agent_command import AgentCommand, AgentCommandError, DeepAgentsModelClient
from .chat_input import ChatInput, ChatInputError
from .config import Settings, configure_logging, load_settings, log_event
from .models import CommandExecutionStatus
from .robot_command import BleakBleClient, RobotCommandError, RobotCommandSender

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DIST_DIR = _PROJECT_ROOT / "dist"


@dataclass(slots=True)
class ChatPipeline:
    """Wired chat → agent → BLE pipeline with injectable boundaries."""

    chat_input: ChatInput
    sender: RobotCommandSender


def _noop_status_callback(status: CommandExecutionStatus) -> None:
    """Contract 1 default: deliberately discard status until U2 integration wires a real consumer.

    The injection point exists so the U2 unit can supply its callback without
    changing this module. Live wiring is explicitly deferred to U2 integration.
    """
    return None


StatusCallback = Callable[[CommandExecutionStatus], None]


def build_pipeline(
    settings: Settings | None = None,
    status_callback: StatusCallback | None = None,
) -> ChatPipeline:
    """Construct the default pipeline. Real LLM/BLE adapters are created, not connected.

    ``status_callback`` is the Contract 1 injection point; when omitted, a
    documented no-op is used (live U2 wiring is deferred to that unit).
    """
    config = settings or load_settings()
    logger = configure_logging(level=config.log_level)
    agent = AgentCommand(
        client=DeepAgentsModelClient(
            api_key=config.openrouter_api_key,
            model=config.openrouter_model,
            base_url=config.openrouter_base_url,
            timeout_s=config.command_timeout_s,
        ),
        logger=logger,
    )
    chat_input = ChatInput(agent=agent, max_length=config.max_chat_length, logger=logger)
    ble_client = BleakBleClient(
        address=config.sphero_device_address,
        service_uuid=config.ble_service_uuid,
        characteristic_uuid=config.ble_command_characteristic_uuid,
    )
    sender = RobotCommandSender(
        ble_client=ble_client,
        status_callback=status_callback or _noop_status_callback,
        logger=logger,
    )
    return ChatPipeline(chat_input=chat_input, sender=sender)


_DEFAULT_PIPELINE: ChatPipeline | None = None


def get_default_pipeline(status_callback: StatusCallback | None = None) -> ChatPipeline:
    """Lazily build (and reuse) the runtime pipeline; settings load happens here."""
    global _DEFAULT_PIPELINE
    if _DEFAULT_PIPELINE is None:
        _DEFAULT_PIPELINE = build_pipeline(status_callback=status_callback)
    return _DEFAULT_PIPELINE


async def health() -> dict[str, str]:
    """Basic liveness endpoint (NFR3.6) — no dependency checks."""
    return {"status": "ok", "service": "u1-chat-command-core"}


def spa_index_response(dist_dir: Path | None = None) -> FileResponse | JSONResponse:
    """Serve the built SPA's index.html, or a helpful 404 when no build exists."""
    dist = dist_dir or _DIST_DIR
    index = dist / "index.html"
    if index.is_file():
        return FileResponse(index)
    return JSONResponse(
        status_code=404,
        content={
            "detail": "SPA build not found. Run 'npm run build' before starting the backend."
        },
    )


def _parse_chat_frame(raw: str) -> str:
    """Accept ``{"text": "..."}`` and legacy plain-text frames."""
    try:
        payload: Any = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(payload, dict):
        return str(payload.get("text", payload.get("command", "")))
    return str(payload)


def _error_response(error: ChatInputError | AgentCommandError | RobotCommandError) -> dict[str, str]:
    """Map a domain error to the chat UI's error envelope (BR1.3)."""
    payload = error.to_chat_error()
    return {
        "type": "error",
        "errorType": payload["type"],
        "message": payload["message"],
        "timestamp": payload["timestamp"],
    }


async def _stop_robot_after_error(sender: RobotCommandSender, log) -> None:
    """Best-effort BLE stop after a command-path error (BR1.3, FR4, AC1.5.2/AC1.5.4).

    Two deliberate exclusions keep the safety rule correct:
    * Input validation failures never reach here — FR3 / AC1.5.1 require a
      rephrase request *before any robot action*, so no BLE stop is issued for
      an unclear message that never reached the agent.
    * A client WebSocket disconnect is a transport lifecycle event, not a robot
      error. The SPA opens a one-shot socket per command and closes it as soon
      as the ack arrives; stopping on that would halt every valid movement.
      A robot BLE disconnect surfaces here as :class:`RobotCommandError` from
      ``sender.send()`` and does trigger the stop path.
    """
    try:
        await sender.stop()
        log_event(log, "robot_stopped_after_error")
    except Exception as exc:  # best effort: the error envelope is still surfaced
        log_event(log, "robot_stop_after_error_failed", error_type=type(exc).__name__)


async def handle_chat_websocket(websocket: WebSocket, pipeline: ChatPipeline, logger=None) -> None:
    """Receive chat frames, execute commands, and stream ack/error responses."""
    log = logger or configure_logging()
    await websocket.accept()
    log_event(log, "chat_connected")
    while True:
        try:
            raw = await websocket.receive_text()
        except WebSocketDisconnect:
            log_event(log, "chat_disconnected")
            return

        text = _parse_chat_frame(raw)
        log_event(log, "chat_frame_received", text_length=len(text))
        try:
            command = await pipeline.chat_input.handle(text)
            status = await pipeline.sender.send(command)
            response = {
                "type": "ack",
                "message": f"Command {command.command.value} accepted.",
                "commandId": command.command_id,
                "status": status.status.value,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except ChatInputError as error:
            # FR3 / AC1.5.1: rephrase before any robot action — no BLE stop here.
            log_event(
                log,
                "chat_error_surfaced",
                error_type=type(error).__name__,
                category=error.code,
            )
            response = _error_response(error)
        except (AgentCommandError, RobotCommandError) as error:
            log_event(
                log,
                "chat_error_surfaced",
                error_type=type(error).__name__,
                category=getattr(error, "code", "error"),
            )
            await _stop_robot_after_error(pipeline.sender, log)
            response = _error_response(error)
        except Exception as exc:  # unexpected backend failure — stop and surface (FR4)
            log_event(log, "chat_unexpected_error", error_type=type(exc).__name__)
            await _stop_robot_after_error(pipeline.sender, log)
            response = _error_response(
                AgentCommandError("Something went wrong controlling the robot. Please try again.")
            )
        await websocket.send_text(json.dumps(response))


def create_app(status_callback: StatusCallback | None = None) -> FastAPI:
    """Build the FastAPI application with health, chat WebSocket, and SPA routes.

    ``status_callback`` is the Contract 1 injection point for U2; leaving it
    unset uses the documented no-op until U2 integration wires the real consumer.
    """
    app = FastAPI(title="Sphero Mini Chat Control", version="0.1.0")

    @app.get("/health")
    async def health_endpoint() -> dict[str, str]:
        return await health()

    @app.websocket("/ws/chat")
    async def chat_endpoint(websocket: WebSocket) -> None:
        await handle_chat_websocket(websocket, get_default_pipeline(status_callback))

    @app.get("/")
    async def spa_root():
        return spa_index_response()

    assets = _DIST_DIR / "assets"
    if assets.is_dir():
        app.mount("/assets", StaticFiles(directory=assets), name="assets")
    return app


app = create_app()
