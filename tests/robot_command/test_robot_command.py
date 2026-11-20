"""BDD scenarios for BLE command execution (AC1.1.x, BR1.3, BR1.4, NFR2.2, NFR4.4).

No Bluetooth stack or robot is involved: every scenario injects a fake BLE client.
"""

from __future__ import annotations

import asyncio
import json
import sys

import pytest

from backend.app import robot_command as robot_module
from backend.app.models import (
    CommandStatus,
    CommandType,
    CommandExecutionStatus,
    RobotCommand,
    SpeedLevel,
)
from backend.app.robot_command import BleakBleClient, BleConnectionError, RobotCommandError

from .conftest import FakeBleClient, make_sender


def forward_command() -> RobotCommand:
    return RobotCommand(command=CommandType.FORWARD, speed=SpeedLevel.MEDIUM)


async def test_given_connected_ble_when_sending_forward_then_payload_is_written_and_status_reported(
    sleeper,
):
    """Given a connected robot, When a movement command is sent, Then BLE receives a JSON payload."""
    # Given
    ble = FakeBleClient(connected=True)
    statuses: list[CommandExecutionStatus] = []
    sender = make_sender(ble, sleeper, statuses.append)
    # When
    result = await sender.send(forward_command())
    # Then
    assert len(ble.writes) == 1
    payload = json.loads(ble.writes[0][2].decode("utf-8"))
    assert payload["command"] == "forward"
    assert payload["speed"] == "medium"
    assert result.status is CommandStatus.MOVING
    assert statuses[0].status is CommandStatus.MOVING
    assert sleeper.delays == []


async def test_given_disconnected_ble_when_sending_then_connection_is_established_first(sleeper):
    """Given a disconnected robot, When sending, Then the sender connects before writing."""
    # Given
    ble = FakeBleClient(connected=False)
    sender = make_sender(ble, sleeper)
    # When
    result = await sender.send(forward_command())
    # Then
    assert ble.connect_calls == 1
    assert len(ble.writes) == 1
    assert result.status is CommandStatus.MOVING


async def test_given_first_write_fails_when_sending_then_reconnect_and_retry_succeeds(sleeper):
    """Given one failed BLE write (NFR4.4), When sending, Then one backoff retry succeeds."""
    # Given
    ble = FakeBleClient(write_errors=(RuntimeError("write failed"), None))
    sender = make_sender(ble, sleeper)
    # When
    result = await sender.send(forward_command())
    # Then
    assert len(ble.writes) == 2
    assert ble.disconnect_calls == 1
    assert ble.connect_calls >= 1
    assert sleeper.delays == pytest.approx([0.1])
    assert result.status is CommandStatus.MOVING


async def test_given_both_writes_fail_when_sending_then_error_is_surfaced(sleeper):
    """Given both BLE attempts fail, When sending, Then no motion is claimed and an error is raised."""
    # Given
    ble = FakeBleClient(write_errors=(RuntimeError("write failed"), RuntimeError("still failed")))
    statuses: list[CommandExecutionStatus] = []
    sender = make_sender(ble, sleeper, statuses.append)
    # When / Then
    with pytest.raises(RobotCommandError, match="unreachable"):
        await sender.send(forward_command())
    assert len(ble.writes) == 2
    assert [status.status for status in statuses] == [CommandStatus.ERROR]


async def test_given_connection_fails_when_sending_then_no_write_is_attempted(sleeper):
    """Given pairing/connection failure (NFR2.2), When sending, Then the robot never moves."""
    # Given
    ble = FakeBleClient(
        connected=False, connect_errors=(BleConnectionError("pairing denied"),) * 3
    )
    sender = make_sender(ble, sleeper)
    # When / Then
    with pytest.raises(RobotCommandError, match="unreachable"):
        await sender.send(forward_command())
    assert ble.writes == []


async def test_given_status_callback_fails_once_when_sending_then_it_is_retried(sleeper):
    """Given U2's callback is briefly unavailable (BR1.4), When sending, Then one retry reports status."""
    # Given
    calls: list[CommandStatus] = []

    def flaky_callback(status: CommandExecutionStatus) -> None:
        calls.append(status.status)
        if len(calls) == 1:
            raise RuntimeError("callback unavailable")

    ble = FakeBleClient()
    sender = make_sender(ble, sleeper, flaky_callback)
    # When
    result = await sender.send(forward_command())
    # Then
    assert result.status is CommandStatus.MOVING
    assert calls == [CommandStatus.MOVING, CommandStatus.MOVING]
    assert sleeper.delays == pytest.approx([0.1])


async def test_given_status_callback_always_fails_when_sending_then_command_still_succeeds(sleeper):
    """Given U2 stays unavailable (BR1.4), When sending, Then U1 logs and continues."""
    # Given
    ble = FakeBleClient()

    def broken_callback(status: CommandExecutionStatus) -> None:
        raise RuntimeError("callback unavailable")

    sender = make_sender(ble, sleeper, broken_callback)
    # When
    result = await sender.send(forward_command())
    # Then
    assert result.status is CommandStatus.MOVING
    assert len(ble.writes) == 1


async def test_given_stop_command_when_sending_then_stopped_status_is_reported(sleeper):
    """Given a stop command (AC1.1.2), When sending, Then status is stopped."""
    # Given
    ble = FakeBleClient()
    sender = make_sender(ble, sleeper)
    stop = RobotCommand(command=CommandType.STOP)
    # When
    result = await sender.send(stop)
    # Then
    assert result.status is CommandStatus.STOPPED
    assert json.loads(ble.writes[0][2].decode("utf-8"))["command"] == "stop"


def test_given_missing_bleak_when_real_client_connects_then_clear_error_is_raised(monkeypatch):
    """Given bleak is not importable, When the real client connects, Then it fails loudly."""
    # Given
    monkeypatch.setitem(sys.modules, "bleak", None)
    client = BleakBleClient("AA:BB:CC:DD:EE:FF", "svc", "char")
    # When / Then
    with pytest.raises(BleConnectionError, match="bleak"):
        asyncio.run(client.connect())


def test_given_fake_bleak_module_when_real_client_is_used_then_calls_are_delegated(monkeypatch):
    """Given an injected bleak module, When the real adapter is used, Then it delegates correctly."""
    # Given
    created: dict[str, object] = {}

    class FakeBleakClient:
        def __init__(self, address) -> None:
            created["address"] = address
            self.is_connected = False

        async def connect(self) -> None:
            created["connected"] = True
            self.is_connected = True

        async def write_gatt_char(self, characteristic, data, response=False) -> None:
            created["write"] = (characteristic, data, response)

        async def disconnect(self) -> None:
            created["disconnected"] = True
            self.is_connected = False

    module = type("FakeModule", (), {"BleakClient": FakeBleakClient})()
    monkeypatch.setitem(sys.modules, "bleak", module)
    client = BleakBleClient("AA:BB:CC:DD:EE:FF", "svc", "char")
    # When
    asyncio.run(client.connect())
    asyncio.run(client.write_gatt("svc", "char", b"payload"))
    connected = asyncio.run(client.is_connected())
    asyncio.run(client.disconnect())
    # Then
    assert connected is True
    assert created["address"] == "AA:BB:CC:DD:EE:FF"
    assert created["write"] == ("char", b"payload", True)
    assert created["disconnected"] is True


async def test_given_unconnected_adapter_when_writing_then_connection_error_is_raised(sleeper):
    """Given no active BLE connection, When writing directly, Then it fails rather than moving."""
    # Given
    client = BleakBleClient("AA:BB:CC:DD:EE:FF", "svc", "char")
    # When / Then
    with pytest.raises(BleConnectionError, match="not connected"):
        await client.write_gatt("svc", "char", b"payload")
