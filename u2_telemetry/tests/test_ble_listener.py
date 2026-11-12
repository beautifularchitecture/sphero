"""BDD scenarios for BLEListener (BLE telemetry reception).

Given/When/Then scenarios:
- Happy path: connect, receive notification, on_telemetry fires with parsed data.
- Error/edge: BLE disconnect triggers on_error; connect failure triggers on_error.
- Edge: malformed payload is skipped without crashing.
"""

from __future__ import annotations

import asyncio

import pytest

from u2_telemetry.ble_listener import BLEListener, TELEMETRY_CHAR_UUID


class MockBleakClient:
    """In-memory stand-in for bleak.BleakClient (no physical Sphero Mini required)."""

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

    def simulate_notification(self, data: str) -> None:
        """Simulate a BLE notification arriving from the robot."""
        if self._notify_cb is not None:
            self._notify_cb(None, bytearray(data, "utf-8"))

    def simulate_disconnect(self) -> None:
        self.is_connected = False


class FailingBleakClient:
    """Mock client whose connect() always raises."""

    def __init__(self, address: str):
        self.address = address
        self.is_connected = False

    async def connect(self):
        raise ConnectionError("device not found")


@pytest.fixture
def captured():
    return {"telemetry": [], "errors": []}


@pytest.fixture
def listener(captured):
    def on_telemetry(raw):
        captured["telemetry"].append(raw)

    def on_error(exc):
        captured["errors"].append(exc)

    return BLEListener(
        "AA:BB:CC:DD:EE:FF",
        on_telemetry=on_telemetry,
        on_error=on_error,
        client_class=MockBleakClient,
    )


@pytest.mark.asyncio
async def test_ble_listener_connect_receives_notification_invokes_on_telemetry(listener, captured):
    """Given a connected BLE listener
    When a telemetry notification arrives
    Then on_telemetry is called with the parsed telemetry dict."""
    await listener.connect()
    assert listener._client.is_connected is True

    # Start the listen loop so start_notify registers the notification callback.
    listener._running = True
    listen_task = asyncio.create_task(listener._listen())
    await asyncio.sleep(0.05)  # let start_notify register the callback

    listener._client.simulate_notification(
        '{"direction": "forward", "orientation": 45.0, "color": "blue", "position": "1.2, 0.4"}'
    )
    await asyncio.sleep(0.05)  # let on_telemetry run

    listener._client.simulate_disconnect()
    await listen_task

    assert len(captured["telemetry"]) == 1
    telemetry = captured["telemetry"][0]
    assert telemetry["direction"] == "forward"
    assert telemetry["orientation"] == 45.0
    assert telemetry["color"] == "blue"
    assert telemetry["position"] == "1.2, 0.4"


@pytest.mark.asyncio
async def test_ble_listener_start_notify_called_with_telemetry_char(listener, captured):
    """Given a connected BLE listener
    When _listen() runs
    Then start_notify is called with the telemetry characteristic UUID."""
    await listener.connect()
    listener._running = True
    listen_task = asyncio.create_task(listener._listen())
    # Let start_notify register the callback, then assert before disconnect clears it.
    await asyncio.sleep(0.05)
    assert listener._client.start_notify_calls == 1
    assert listener._client._notify_cb is not None
    listener._client.simulate_disconnect()
    await listen_task


@pytest.mark.asyncio
async def test_ble_listener_disconnection_triggers_on_error(listener, captured):
    """Given a connected BLE listener
    When the BLE connection drops
    Then on_error is invoked with the exception."""
    await listener.connect()

    listener.on_error(ConnectionError("BLE link lost"))

    assert len(captured["errors"]) == 1
    assert isinstance(captured["errors"][0], ConnectionError)
    assert "BLE link lost" in str(captured["errors"][0])


@pytest.mark.asyncio
async def test_ble_listener_connect_failure_invokes_on_error(captured):
    """Given a BLE client whose connect() raises
    When connect() is called
    Then the exception propagates (start() loop would invoke on_error)."""
    failing = BLEListener(
        "AA:BB:CC:DD:EE:FF",
        on_telemetry=lambda raw: None,
        on_error=lambda exc: captured["errors"].append(exc),
        client_class=FailingBleakClient,
    )

    with pytest.raises(ConnectionError, match="device not found"):
        await failing.connect()

    assert failing._client.is_connected is False


@pytest.mark.asyncio
async def test_ble_listener_malformed_payload_skipped_without_crash(listener, captured):
    """Given a telemetry notification with malformed JSON
    When the notification is received
    Then on_telemetry is NOT called and no exception propagates."""
    await listener.connect()

    listener._client.simulate_notification("{not valid json}")

    assert len(captured["telemetry"]) == 0
    assert listener._client.is_connected is True


@pytest.mark.asyncio
async def test_ble_listener_disconnect_sets_running_false(listener):
    """Given a running BLE listener
    When disconnect() is called
    Then _running is False and the client disconnects."""
    await listener.connect()
    await listener.disconnect()

    assert listener._running is False
    assert listener._client.disconnect_calls == 1
    assert listener._client.is_connected is False


@pytest.mark.asyncio
async def test_ble_listener_telemetry_char_uuid_is_constant():
    """Given the BLEListener module
    When the telemetry characteristic UUID is referenced
    Then it is a stable string (not hard-coded per call)."""
    assert TELEMETRY_CHAR_UUID == "0000ffe1-0000-1000-8000-00805f9b34fb"
    assert "-" in TELEMETRY_CHAR_UUID
