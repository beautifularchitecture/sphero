"""Contract 2 and NFR2.3 reliability scenarios for the event bus and BLE retry.

Given/When/Then scenarios:
- Happy path: event bus publish delivers a RobotStateChanged event to a
  WebSocket-like subscriber; the payload carries the correlation_id.
- Error/edge: a failing subscriber is removed and does not block the others;
  an unknown topic is ignored and no subscriber receives a message.
- Correlation id: RobotState carries an auto-generated, unique correlation_id
  that is propagated into the published event payload.
- BLE retry: BLEListener.start() stops after 3 connect failures (NFR2.3)
  instead of entering a tight unbounded retry loop.
"""

from __future__ import annotations

import asyncio
import json

import pytest

from u2_telemetry.ble_listener import BLEListener
from u2_telemetry.event_bus import RobotStateEventBus, TOPIC
from u2_telemetry.models import RobotState


class CaptureSubscriber:
    """WebSocket-like subscriber capturing every text message sent to it."""

    def __init__(self, fail: bool = False) -> None:
        self.messages: list[str] = []
        self.fail = fail

    async def send_text(self, message: str) -> None:
        if self.fail:
            raise RuntimeError("send failed")
        self.messages.append(message)


class FailingBleakClient:
    """Mock client whose connect() always raises (no physical Sphero Mini).

    Records every connect attempt on the shared ``attempts`` counter because
    each reconnect instantiates a fresh client.
    """

    def __init__(self, address: str, attempts: dict) -> None:
        self.address = address
        self.is_connected = False
        self.attempts = attempts

    async def connect(self):
        self.attempts["n"] += 1
        raise ConnectionError("device not found")


@pytest.fixture
def bus():
    return RobotStateEventBus()


def make_state(correlation_id: str = "corr-1") -> RobotState:
    return RobotState(
        stateId="s-1",
        direction="forward",
        orientation=45.0,
        color="blue",
        position="1.2, 0.4",
        timestamp="2026-11-12T00:00:00+00:00",
        correlation_id=correlation_id,
    )


@pytest.mark.asyncio
async def test_event_bus_publish_delivers_to_subscriber(bus):
    """Given an event bus with a subscriber
    When publish() is called with a RobotState
    Then the subscriber receives the robot.state.changed message."""
    sub = CaptureSubscriber()
    await bus.subscribe(sub)
    await bus.publish(TOPIC, make_state())

    assert len(sub.messages) == 1
    payload = json.loads(sub.messages[0])
    assert payload["topic"] == TOPIC
    assert payload["state"]["stateId"] == "s-1"
    assert payload["state"]["direction"] == "forward"


@pytest.mark.asyncio
async def test_event_bus_published_payload_carries_correlation_id(bus):
    """Given a RobotState with a correlation_id
    When it is published on the bus
    Then the delivered payload carries the same correlation_id."""
    sub = CaptureSubscriber()
    await bus.subscribe(sub)
    await bus.publish(TOPIC, make_state(correlation_id="corr-abc"))

    payload = json.loads(sub.messages[0])
    assert payload["state"]["correlation_id"] == "corr-abc"


@pytest.mark.asyncio
async def test_event_bus_failing_subscriber_is_removed(bus):
    """Given one subscriber that raises and one healthy subscriber
    When publish() is called
    Then the failing subscriber is removed and the healthy one still receives."""
    failing = CaptureSubscriber(fail=True)
    healthy = CaptureSubscriber()
    await bus.subscribe(failing)
    await bus.subscribe(healthy)
    await bus.publish(TOPIC, make_state())

    assert len(healthy.messages) == 1
    assert failing not in bus._subscribers


@pytest.mark.asyncio
async def test_event_bus_unknown_topic_ignored(bus):
    """Given publish() on a topic other than robot.state.changed
    When publish() is called
    Then no subscriber receives a message."""
    sub = CaptureSubscriber()
    await bus.subscribe(sub)
    await bus.publish("other.topic", make_state())

    assert len(sub.messages) == 0


def test_robot_state_correlation_id_auto_generated():
    """Given a RobotState built without a correlation_id
    When it is constructed
    Then a non-empty correlation_id is auto-generated."""
    state = RobotState(
        stateId="s-1",
        direction="forward",
        orientation=0.0,
        color="red",
        position="0,0",
        timestamp="2026-11-12T00:00:00+00:00",
    )
    assert state.correlation_id != ""


def test_robot_state_correlation_id_unique_per_reading():
    """Given two RobotState readings
    When each is constructed
    Then each has a unique correlation_id."""
    first = RobotState(
        stateId="s-1",
        direction="forward",
        orientation=0.0,
        color="red",
        position="0,0",
        timestamp="2026-11-12T00:00:00+00:00",
    )
    second = RobotState(
        stateId="s-2",
        direction="forward",
        orientation=0.0,
        color="red",
        position="0,0",
        timestamp="2026-11-12T00:00:00+00:00",
    )
    assert first.correlation_id != second.correlation_id


def test_robot_state_correlation_id_can_be_supplied():
    """Given a correlation_id supplied at construction
    When the RobotState is constructed
    Then the supplied value is used."""
    state = RobotState(
        stateId="s-1",
        direction="forward",
        orientation=0.0,
        color="red",
        position="0,0",
        timestamp="2026-11-12T00:00:00+00:00",
        correlation_id="corr-supplied",
    )
    assert state.correlation_id == "corr-supplied"


@pytest.mark.asyncio
async def test_ble_listener_start_stops_after_three_connect_failures():
    """Given a BLE client whose connect() always raises
    When start() is run
    Then it attempts 3 connects, signals on_error each time, and stops
    instead of looping (NFR2.3)."""
    attempts = {"n": 0}
    errors = []
    listener = BLEListener(
        "AA:BB:CC:DD:EE:FF",
        on_telemetry=lambda raw: None,
        on_error=lambda exc: errors.append(exc),
        client_class=lambda addr: FailingBleakClient(addr, attempts),
    )

    task = asyncio.create_task(listener.start())
    await asyncio.sleep(3.5)  # 3 connects + 1s + 2s backoff
    listener._running = False
    await asyncio.sleep(0.1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

    assert listener._running is False
    assert attempts["n"] == 3  # exactly 3 connect attempts, then stop (NFR2.3)
    assert len(errors) == 3  # each failure signaled to the error handler
