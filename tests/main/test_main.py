"""BDD scenarios for the FastAPI entrypoint (NFR3.6, BR1.3, endpoint/error coverage).

The WebSocket handler is exercised directly with a fake socket, so no ASGI test
client (and therefore no ``httpx`` installation) is required.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse

from backend.app import main as main_module
from backend.app.agent_command import AgentCommandError
from backend.app.chat_input import ChatInputError
from backend.app.config import Settings
from backend.app.models import (
    CommandExecutionStatus,
    CommandSource,
    CommandStatus,
    CommandType,
    RobotCommand,
)
from backend.app.robot_command import RobotCommandError


class FakeWebSocket:
    def __init__(self, *messages: str) -> None:
        self.incoming = list(messages)
        self.sent: list[str] = []
        self.accepted = False
        self.closed = False

    async def accept(self) -> None:
        self.accepted = True

    async def receive_text(self) -> str:
        if not self.incoming:
            raise WebSocketDisconnect(code=1000)
        return self.incoming.pop(0)

    async def send_text(self, payload: str) -> None:
        self.sent.append(payload)

    async def close(self, code: int = 1000) -> None:
        self.closed = True


class FakeChatInput:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.calls: list[str] = []

    async def handle(self, text, source=None):
        self.calls.append(text)
        if self.error is not None:
            raise self.error
        return RobotCommand(command=CommandType.FORWARD)


class FakeSender:
    def __init__(self, error: Exception | None = None, stop_error: Exception | None = None) -> None:
        self.error = error
        self.stop_error = stop_error
        self.calls: list[RobotCommand] = []
        self.stops: list[RobotCommand] = []

    async def send(self, command):
        self.calls.append(command)
        if self.error is not None:
            raise self.error
        return CommandExecutionStatus(command_id=command.command_id, status=CommandStatus.MOVING)

    async def stop(self):
        self.stops.append(RobotCommand(command=CommandType.STOP, source=CommandSource.API))
        if self.stop_error is not None:
            raise self.stop_error


def pipeline(chat_error=None, sender_error=None, stop_error=None):
    return SimpleNamespace(
        chat_input=FakeChatInput(chat_error),
        sender=FakeSender(sender_error, stop_error),
    )


async def test_given_backend_is_running_when_health_is_checked_then_ok_is_returned():
    """Given the app is up, When /health is called, Then a 200-style liveness body is returned."""
    body = await main_module.health()
    assert body["status"] == "ok"
    assert body["service"] == "u1-chat-command-core"


async def test_given_valid_json_chat_when_websocket_handles_it_then_ack_is_sent():
    """Given a JSON chat frame, When handled, Then an ack with the command status is sent."""
    # Given
    socket = FakeWebSocket('{"text":"roll forward"}')
    injected = pipeline()
    # When
    await main_module.handle_chat_websocket(socket, injected)  # type: ignore[arg-type]
    # Then
    assert socket.accepted is True
    assert len(socket.sent) == 1
    ack = json.loads(socket.sent[0])
    assert ack["type"] == "ack"
    assert ack["status"] == "moving"
    assert injected.chat_input.calls == ["roll forward"]
    assert len(injected.sender.calls) == 1


async def test_given_plain_text_chat_when_websocket_handles_it_then_ack_is_sent():
    """Given a legacy plain-text frame, When handled, Then it is accepted as chat text."""
    # Given
    socket = FakeWebSocket("stop")
    injected = pipeline()
    # When
    await main_module.handle_chat_websocket(socket, injected)  # type: ignore[arg-type]
    # Then
    assert injected.chat_input.calls == ["stop"]
    assert json.loads(socket.sent[0])["type"] == "ack"


async def test_given_invalid_chat_when_websocket_handles_it_then_rephrase_error_is_sent():
    """Given invalid chat (BR1.1), When handled, Then the error reaches the UI and no BLE write occurs."""
    # Given
    socket = FakeWebSocket('{"text":"dance"}')
    injected = pipeline(chat_error=ChatInputError("Please rephrase your command."))
    # When
    await main_module.handle_chat_websocket(socket, injected)  # type: ignore[arg-type]
    # Then
    error = json.loads(socket.sent[0])
    assert error["type"] == "error"
    assert error["errorType"] == "validation"
    assert "rephrase" in error["message"].lower()
    assert injected.sender.calls == []
    # FR3 / AC1.5.1: an unclear message triggers a rephrase before any robot action.
    assert injected.sender.stops == []


async def test_given_agent_failure_when_websocket_handles_it_then_agent_error_is_sent():
    """Given translation fails (FR4), When handled, Then a typed agent error is sent."""
    # Given
    socket = FakeWebSocket('{"text":"roll forward"}')
    injected = pipeline(chat_error=AgentCommandError("language service unavailable"))
    # When
    await main_module.handle_chat_websocket(socket, injected)  # type: ignore[arg-type]
    # Then
    error = json.loads(socket.sent[0])
    assert error["errorType"] == "agent_error"
    assert injected.sender.calls == []
    # BR1.3 / AC1.5.2: agent uncertainty stops the robot, not just the chat text.
    assert len(injected.sender.stops) == 1
    assert injected.sender.stops[0].command is CommandType.STOP


async def test_given_bluetooth_failure_when_websocket_handles_it_then_bluetooth_error_is_sent():
    """Given the robot is unreachable (NFR2.2), When handled, Then a typed BLE error is sent."""
    # Given
    socket = FakeWebSocket('{"text":"roll forward"}')
    injected = pipeline(sender_error=RobotCommandError("robot unreachable"))
    # When
    await main_module.handle_chat_websocket(socket, injected)  # type: ignore[arg-type]
    # Then
    error = json.loads(socket.sent[0])
    assert error["errorType"] == "bluetooth"
    assert "unreachable" in error["message"]
    # BR1.3 / AC1.5.4: a robot disconnect must command a BLE stop.
    assert len(injected.sender.stops) == 1
    assert injected.sender.stops[0].command is CommandType.STOP


async def test_given_unexpected_backend_failure_when_websocket_handles_it_then_robot_stops_and_error_is_sent():
    """Given an unhandled backend error, When handled, Then the robot stops and an error is surfaced (FR4)."""
    # Given
    socket = FakeWebSocket('{"text":"roll forward"}')
    injected = pipeline(sender_error=RuntimeError("database gone"))
    # When
    await main_module.handle_chat_websocket(socket, injected)  # type: ignore[arg-type]
    # Then
    error = json.loads(socket.sent[0])
    assert error["type"] == "error"
    assert error["errorType"] == "agent_error"
    assert "Something went wrong" in error["message"]
    assert len(injected.sender.stops) == 1


async def test_given_stop_itself_fails_when_an_error_occurs_then_the_error_is_still_surfaced():
    """Given the BLE stop fails, When an agent error occurs, Then the chat error is still sent."""
    # Given
    socket = FakeWebSocket('{"text":"roll forward"}')
    injected = pipeline(
        chat_error=AgentCommandError("language service unavailable"),
        stop_error=RobotCommandError("robot unreachable"),
    )
    # When
    await main_module.handle_chat_websocket(socket, injected)  # type: ignore[arg-type]
    # Then
    error = json.loads(socket.sent[0])
    assert error["errorType"] == "agent_error"
    assert len(injected.sender.stops) == 1


async def test_given_client_disconnects_when_websocket_handles_it_then_loop_ends_cleanly():
    """Given no further frames, When the client disconnects, Then the handler returns quietly."""
    # Given
    socket = FakeWebSocket()
    injected = pipeline()
    # When
    await main_module.handle_chat_websocket(socket, injected)  # type: ignore[arg-type]
    # Then
    assert socket.sent == []
    assert injected.chat_input.calls == []


def test_given_built_spa_when_index_is_requested_then_index_html_is_served(tmp_path):
    """Given dist/index.html exists, When the SPA route responds, Then a FileResponse is returned."""
    # Given
    index = tmp_path / "index.html"
    index.write_text("<html>sphero</html>", encoding="utf-8")
    # When
    response = main_module.spa_index_response(tmp_path)
    # Then
    assert isinstance(response, FileResponse)
    assert Path(response.path) == index


def test_given_no_spa_build_when_index_is_requested_then_helpful_404_is_returned(tmp_path):
    """Given no build output, When the SPA route responds, Then a helpful 404 is returned."""
    # When
    response = main_module.spa_index_response(tmp_path)
    # Then
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404


def test_given_configured_settings_when_pipeline_is_built_then_chat_and_ble_are_wired():
    """Given settings, When the default pipeline is built, Then both injected boundaries exist."""
    # Given
    settings = Settings(openrouter_api_key="sk-or-test", sphero_device_address="AA:BB:CC:DD:EE:FF")
    # When
    built = main_module.build_pipeline(settings)
    # Then
    assert hasattr(built.chat_input, "handle")
    assert hasattr(built.sender, "send")
    assert "sk-or-test" not in repr(built)


def test_given_app_factory_when_app_is_created_then_expected_routes_are_registered():
    """Given the factory, When the app is created, Then health, chat WS and SPA routes exist."""
    app = main_module.create_app()
    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/health" in paths
    assert "/ws/chat" in paths
    assert "/" in paths


def test_given_no_callback_when_pipeline_is_built_then_contract1_defaults_to_noop():
    """Given no injection, When the pipeline is built, Then Contract 1 uses the documented no-op."""
    # Given
    settings = Settings(openrouter_api_key="sk-or-test", sphero_device_address="AA:BB:CC:DD:EE:FF")
    # When
    built = main_module.build_pipeline(settings)
    # Then
    assert built.sender._status_callback is main_module._noop_status_callback
    built.sender._status_callback(CommandExecutionStatus(command_id="cmd-x", status=CommandStatus.MOVING))


def test_given_injected_callback_when_pipeline_is_built_then_contract1_wires_it():
    """Given a U2 callback, When the pipeline is built, Then the sender reports through it."""
    # Given
    settings = Settings(openrouter_api_key="sk-or-test", sphero_device_address="AA:BB:CC:DD:EE:FF")
    received: list[CommandExecutionStatus] = []
    # When
    built = main_module.build_pipeline(settings, status_callback=received.append)
    # Then — a bound method is a fresh object on every attribute access, so assert
    # the injected callback's behaviour rather than `is received.append`.
    assert callable(built.sender._status_callback)
    assert built.sender._status_callback is not main_module._noop_status_callback
    built.sender._status_callback(CommandExecutionStatus(command_id="cmd-y", status=CommandStatus.STOPPED))
    assert [item.command_id for item in received] == ["cmd-y"]
    assert received[0].status is CommandStatus.STOPPED
