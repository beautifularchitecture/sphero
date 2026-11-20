"""BDD scenarios for LED colour translation (AC1.3.1–AC1.3.3, FR2, BR1.2)."""

from __future__ import annotations

import pytest

from backend.app.agent_command import AgentCommandError
from backend.app.models import CommandType, ColorValue

from .conftest import ScriptedModelClient, translate


@pytest.mark.parametrize(
    ("chat", "color", "ac_id"),
    [
        ("set color red", "red", "AC1.3.1"),
        ("set color blue", "blue", "AC1.3.2"),
        ("set color green", "green", "AC1.3.3"),
    ],
)
async def test_given_color_chat_when_translating_then_setcolor_command_carries_color(
    sleeper, chat, color, ac_id
):
    """Given each colour phrase, When translated, Then command=setColor with that colour."""
    # Given
    client = ScriptedModelClient('{"command":"setColor","color":"' + color + '"}')
    # When
    command = await translate(client, sleeper, chat)
    # Then
    assert command.command is CommandType.SET_COLOR, ac_id
    assert command.color is ColorValue(color), ac_id
    assert command.speed is None


async def test_given_setcolor_without_color_when_translating_then_rephrase_error_is_raised(sleeper):
    """Given setColor with no colour value, When translated, Then the output is rejected."""
    # Given
    client = ScriptedModelClient('{"command":"setColor"}')
    # When / Then
    with pytest.raises(AgentCommandError, match="rephrase"):
        await translate(client, sleeper, "set color")


async def test_given_invalid_color_value_when_translating_then_rephrase_error_is_raised(sleeper):
    """Given a colour outside red/blue/green, When translated, Then it is rejected."""
    # Given
    client = ScriptedModelClient('{"command":"setColor","color":"purple"}')
    # When / Then
    with pytest.raises(AgentCommandError, match="rephrase"):
        await translate(client, sleeper, "set color purple")
