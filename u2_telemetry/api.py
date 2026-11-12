"""FastAPI app exposing Contract 2 RobotStateChanged events via WebSocket.

Requires ``fastapi`` and ``uvicorn`` (declared dependencies in
``pyproject.toml``). Imported lazily from ``__main__`` so the package remains
importable when the transport stack is not installed.

The WebSocket endpoint ``/ws/robot-state`` accepts subscribers and the shared
``RobotStateEventBus`` broadcasts each normalized ``RobotState`` to them, so
events leave the publisher queue and reach U3 StatsDisplay (Contract 2).

The bus is injected from ``__main__`` via :func:`set_event_bus` so the service
(which publishes via ``event_bus_publish=bus.publish``) and this endpoint
(which subscribes to this bus) share the SAME ``RobotStateEventBus`` instance.
Without that wiring, `__main__` and `api` would each build their own bus and
Contract 2 delivery would break end-to-end.
"""

from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from .event_bus import RobotStateEventBus

app = FastAPI(title="U2 RobotTelemetry")

# Shared RobotStateEventBus instance. Injected from __main__ via
# set_event_bus() so the WebSocket endpoint subscribes to the SAME bus the
# RobotTelemetryService publishes to (Contract 2). Defaults to a standalone
# instance so the module stays importable and unit-testable without the
# transport stack; __main__ overrides it with the application's single shared
# bus before serving.
_bus: RobotStateEventBus | None = None


def set_event_bus(bus_instance: RobotStateEventBus) -> None:
    """Inject the shared event bus used by the WebSocket endpoint."""
    global _bus
    _bus = bus_instance


def _get_bus() -> RobotStateEventBus:
    """Return the injected bus, lazily creating a default if none is set."""
    global _bus
    if _bus is None:
        _bus = RobotStateEventBus()
    return _bus


@app.websocket("/ws/robot-state")
async def robot_state_changed(websocket: WebSocket) -> None:
    """WebSocket endpoint delivering RobotStateChanged events to U3 StatsDisplay."""
    target_bus = _get_bus()
    await target_bus.subscribe(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await target_bus.unsubscribe(websocket)
