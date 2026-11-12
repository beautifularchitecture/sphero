"""BDD scenarios for the FastAPI WebSocket endpoint (Contract 2).

Given/When/Then scenarios:
- Happy path: a WebSocket client subscribed to the shared bus receives a
  RobotStateChanged event published to that bus.
- Error/edge: publishing on an unknown topic delivers to no subscriber.
- Edge: set_event_bus() injection makes the endpoint subscribe to the
  injected (shared) bus rather than a separate per-module instance.
- Edge: when no bus is injected, _get_bus() lazily creates a standalone bus
  so the module stays importable and testable without the transport stack.
"""

from __future__ import annotations

import asyncio
import json

import pytest
from fastapi import WebSocketDisconnect

import u2_telemetry.api as api_module
from u2_telemetry.api import _get_bus, robot_state_changed, set_event_bus
from u2_telemetry.event_bus import RobotStateEventBus, TOPIC
from u2_telemetry.models import RobotState


class FakeWebSocket:
    """Minimal WebSocket stand-in: records sent messages, blocks on receive."""

    def __init__(self) -> None:
        self.received: list[str] = []
        self._unblock = asyncio.Event()

    async def accept(self) -> None:
        return None

    async def receive_text(self) -> str:
        await self._unblock.wait()
        raise WebSocketDisconnect()

    async def send_text(self, message: str) -> None:
        self.received.append(message)

    def close(self) -> None:
        self._unblock.set()


def make_state() -> RobotState:
    return RobotState(
        stateId="s-1",
        direction="forward",
        orientation=45.0,
        color="blue",
        position="1.2, 0.4",
        timestamp="2026-11-12T00:00:00+00:00",
        correlation_id="corr-1",
    )


@pytest.fixture(autouse=True)
def reset_api_bus():
    """Each test starts with no bus injected, for isolation."""
    api_module._bus = None
    yield
    api_module._bus = None


@pytest.fixture
def shared_bus() -> RobotStateEventBus:
    return RobotStateEventBus()


@pytest.mark.asyncio
async def test_endpoint_subscribes_to_injected_shared_bus(shared_bus):
    """Given set_event_bus() is called with a bus instance
    When _get_bus() is called
    Then it returns that same injected instance (single shared bus, DI)."""
    set_event_bus(shared_bus)
    assert _get_bus() is shared_bus


@pytest.mark.asyncio
async def test_endpoint_creates_default_bus_when_none_injected():
    """Given set_event_bus() was never called
    When _get_bus() is called
    Then it lazily creates a standalone bus and caches it."""
    bus = _get_bus()
    assert isinstance(bus, RobotStateEventBus)
    assert _get_bus() is bus  # cached after first creation


@pytest.mark.asyncio
async def test_websocket_client_receives_published_event(shared_bus):
    """Given a WebSocket client connected to /ws/robot-state on the shared bus
    When a RobotStateChanged event is published to that bus
    Then the client receives the robot.state.changed message."""
    set_event_bus(shared_bus)
    ws = FakeWebSocket()
    task = asyncio.create_task(robot_state_changed(ws))
    await asyncio.sleep(0.05)  # let subscribe() complete

    await shared_bus.publish(TOPIC, make_state())
    await asyncio.sleep(0.05)  # let delivery complete

    assert len(ws.received) == 1
    payload = json.loads(ws.received[0])
    assert payload["topic"] == TOPIC
    assert payload["state"]["stateId"] == "s-1"
    assert payload["state"]["direction"] == "forward"

    ws.close()
    await task
    # Subscriber removed on disconnect so it cannot stall later delivery.
    assert ws not in shared_bus._subscribers


@pytest.mark.asyncio
async def test_unknown_topic_delivers_to_no_subscriber(shared_bus):
    """Given publish() on a topic other than robot.state.changed
    When publish() is called
    Then no subscriber receives a message."""
    set_event_bus(shared_bus)
    ws = FakeWebSocket()
    task = asyncio.create_task(robot_state_changed(ws))
    await asyncio.sleep(0.05)  # let subscribe() complete

    await shared_bus.publish("other.topic", make_state())
    await asyncio.sleep(0.05)

    assert ws.received == []

    ws.close()
    await task
