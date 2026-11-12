"""BDD integration scenarios for RobotTelemetryService (end-to-end telemetry path).

Given/When/Then scenarios:
- Happy path: BLE telemetry → normalize → publish → event received by subscriber.
- Error/edge: BLE error signals U1; lenient normalization in service flow.
- Edge: CommandExecutionStatus callback from U1 recorded; service start/stop lifecycle.
"""

from __future__ import annotations

import asyncio

import pytest

from u2_telemetry.ble_listener import BLEListener
from u2_telemetry.models import RobotState
from u2_telemetry.service import RobotTelemetryService


class MockBleakClient:
    def __init__(self, address: str):
        self.address = address
        self.is_connected = False
        self.connect_calls = 0
        self.disconnect_calls = 0
        self.start_notify_calls = 0
        self.stop_notify_calls = 0
        self._notify_cb = None

    async def connect(self):
        self.connect_calls += 1
        self.is_connected = True

    async def disconnect(self):
        self.disconnect_calls += 1
        self.is_connected = False

    async def start_notify(self, char_uuid, callback):
        self.start_notify_calls += 1
        self._notify_cb = callback

    async def stop_notify(self, char_uuid):
        self.stop_notify_calls += 1
        self._notify_cb = None

    def simulate_notification(self, data: str):
        if self._notify_cb is not None:
            self._notify_cb(None, bytearray(data, "utf-8"))

    def simulate_disconnect(self) -> None:
        self.is_connected = False


@pytest.fixture
def svc():
    published = []
    errors = []
    statuses = []

    async def publish(topic, state):
        published.append((topic, state))

    service = RobotTelemetryService(
        ble_address="AA:BB:CC:DD:EE:FF",
        event_bus_publish=publish,
        u1_status_callback=lambda command_id, status, timestamp: statuses.append(
            (command_id, status, timestamp)
        ),
        u1_error_signal=lambda exc: errors.append(exc),
        client_class=MockBleakClient,
    )
    service._published = published
    service._errors = errors
    service._statuses = statuses
    return service


async def _connect_listener(service):
    """Connect the service's BLE listener (mock hardware) so notifications can be simulated."""
    service._listener = BLEListener(
        service.ble_address,
        on_telemetry=service._on_telemetry,
        on_error=service.connection.handle_error,
        client_class=service._client_class,
    )
    await service._listener.connect()
    service._listener._running = True
    service._listen_task = asyncio.create_task(service._listener._listen())
    await asyncio.sleep(0.05)  # let start_notify register the callback


@pytest.mark.asyncio
async def test_service_ble_telemetry_normalizes_and_publishes(svc):
    """Given a RobotTelemetryService with mocks wired
    When a BLE telemetry notification arrives
    Then the telemetry is normalized and a RobotStateChanged event is published."""
    await svc.publisher.start()
    await _connect_listener(svc)
    svc._listener._client.simulate_notification(
        '{"direction": "forward", "orientation": 45.0, "color": "blue", "position": "1.2, 0.4"}'
    )
    await asyncio.sleep(0.1)  # let the enqueue task run
    svc._listener._client.simulate_disconnect()
    await svc._listen_task
    await svc.publisher.stop()

    assert len(svc._published) == 1
    topic, state = svc._published[0]
    assert topic == "robot.state.changed"
    assert isinstance(state, RobotState)
    assert state.direction == "forward"
    assert state.orientation == 45.0
    assert state.color == "blue"
    assert state.position == "1.2, 0.4"
    assert state.timestamp != ""


@pytest.mark.asyncio
async def test_service_lenient_normalization_partial_telemetry(svc):
    """Given partial telemetry missing fields
    When a BLE notification arrives
    Then the service still emits a RobotState with placeholder values (not blocked)."""
    await svc.publisher.start()
    await _connect_listener(svc)
    svc._listener._client.simulate_notification('{"direction": "forward"}')
    await asyncio.sleep(0.1)
    svc._listener._client.simulate_disconnect()
    await svc._listen_task
    await svc.publisher.stop()

    assert len(svc._published) == 1
    _, state = svc._published[0]
    assert state.direction == "forward"
    assert state.orientation is None
    assert state.color == "-"
    assert state.position == "-"


@pytest.mark.asyncio
async def test_service_ble_error_signals_u1(svc):
    """Given a service whose BLE listener errors
    When handle_error is invoked on the connection handler
    Then the error is signaled to U1 (errors list)."""
    await svc.connection.handle_error(ConnectionError("BLE disconnect"))

    assert len(svc._errors) == 1
    assert isinstance(svc._errors[0], ConnectionError)
    assert "BLE disconnect" in str(svc._errors[0])


@pytest.mark.asyncio
async def test_service_command_status_from_u1_is_recorded(svc):
    """Given U1 invokes the CommandExecutionStatus sync callback
    When handle_command_status() is called
    Then the status is recorded and retrievable."""
    svc.handle_command_status("cmd-1", "moving", "2026-11-12T10:00:00+00:00")

    record = svc.status_handler.get_status("cmd-1")
    assert record is not None
    assert record["status"] == "moving"


@pytest.mark.asyncio
async def test_service_start_stop_lifecycle(svc):
    """Given a RobotTelemetryService
    When run() is started then stopped
    Then the publisher and listener lifecycle is managed cleanly."""
    task = asyncio.create_task(svc.run())
    await asyncio.sleep(0.05)
    assert svc._listener is not None
    assert svc.publisher._task is not None
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    await svc.stop()


@pytest.mark.asyncio
async def test_service_multiple_telemetry_events_published(svc):
    """Given multiple BLE notifications
    When each arrives
    Then each produces a published RobotStateChanged event."""
    await svc.publisher.start()
    await _connect_listener(svc)
    svc._listener._client.simulate_notification(
        '{"direction": "forward", "orientation": 10.0, "color": "red", "position": "0,0"}'
    )
    svc._listener._client.simulate_notification(
        '{"direction": "backward", "orientation": 20.0, "color": "blue", "position": "1,1"}'
    )
    await asyncio.sleep(0.1)
    svc._listener._client.simulate_disconnect()
    await svc._listen_task
    await svc.publisher.stop()

    assert len(svc._published) == 2
    assert svc._published[0][1].direction == "forward"
    assert svc._published[1][1].direction == "backward"
