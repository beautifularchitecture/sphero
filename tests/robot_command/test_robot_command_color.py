"""BDD scenarios for sending LED colour commands over BLE (AC1.3.1–AC1.3.3)."""

from __future__ import annotations

import json

import pytest

from backend.app.models import ColorValue, CommandSource, CommandType, RobotCommand

from .conftest import FakeBleClient, make_sender


@pytest.mark.parametrize(
    ("color", "ac_id"),
    [("red", "AC1.3.1"), ("blue", "AC1.3.2"), ("green", "AC1.3.3")],
)
async def test_given_setcolor_command_when_sent_over_ble_then_payload_carries_color(
    sleeper, color, ac_id
):
    """Given each LED colour, When sent over BLE, Then the encoded payload includes it."""
    # Given
    ble = FakeBleClient()
    sender = make_sender(ble, sleeper)
    command = RobotCommand(
        command=CommandType.SET_COLOR, color=ColorValue(color), source=CommandSource.BUTTON
    )
    # When
    result = await sender.send(command)
    # Then
    payload = json.loads(ble.writes[0][2].decode("utf-8"))
    assert payload["command"] == "setColor", ac_id
    assert payload["color"] == color, ac_id
    assert result.command_id == command.command_id
