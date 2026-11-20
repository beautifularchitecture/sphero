"""BDD scenarios for sending speed commands over BLE (AC1.2.1–AC1.2.3)."""

from __future__ import annotations

import json

import pytest

from backend.app.models import CommandSource, CommandType, RobotCommand, SpeedLevel

from .conftest import FakeBleClient, make_sender


@pytest.mark.parametrize(
    ("level", "ac_id"),
    [("low", "AC1.2.1"), ("medium", "AC1.2.2"), ("high", "AC1.2.3")],
)
async def test_given_setspeed_command_when_sent_over_ble_then_payload_carries_level(
    sleeper, level, ac_id
):
    """Given each speed level, When sent over BLE, Then the encoded payload includes it."""
    # Given
    ble = FakeBleClient()
    sender = make_sender(ble, sleeper)
    command = RobotCommand(
        command=CommandType.SET_SPEED, speed=SpeedLevel(level), source=CommandSource.BUTTON
    )
    # When
    result = await sender.send(command)
    # Then
    payload = json.loads(ble.writes[0][2].decode("utf-8"))
    assert payload["command"] == "setSpeed", ac_id
    assert payload["speed"] == level, ac_id
    assert result.command_id == command.command_id


@pytest.mark.parametrize(
    ("level", "ac_id"),
    [("low", "AC1.2.1"), ("medium", "AC1.2.2"), ("high", "AC1.2.3")],
)
async def test_given_movement_with_configured_speed_when_sent_over_ble_then_payload_keeps_level(
    sleeper, level, ac_id
):
    """Given a movement carrying the configured speed, When sent, Then BLE keeps it (no medium overwrite)."""
    # Given
    ble = FakeBleClient()
    sender = make_sender(ble, sleeper)
    command = RobotCommand(
        command=CommandType.FORWARD, speed=SpeedLevel(level), source=CommandSource.CHAT
    )
    # When
    await sender.send(command)
    # Then
    payload = json.loads(ble.writes[0][2].decode("utf-8"))
    assert payload["command"] == "forward", ac_id
    assert payload["speed"] == level, ac_id
