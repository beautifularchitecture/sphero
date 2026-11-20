"""BDD scenarios for speed translation (AC1.2.1–AC1.2.3, FR1.2, BR1.2).

The requirement is about *subsequent movement*: a setSpeed command must govern
the speed of later movement commands, not merely carry the level itself.
"""

from __future__ import annotations

import pytest

from backend.app.agent_command import AgentCommandError
from backend.app.models import CommandSource, CommandType, SpeedLevel

from .conftest import ScriptedModelClient, make_agent, translate


@pytest.mark.parametrize(
    ("chat", "level", "ac_id"),
    [
        ("set speed low", "low", "AC1.2.1"),
        ("set speed medium", "medium", "AC1.2.2"),
        ("set speed high", "high", "AC1.2.3"),
    ],
)
async def test_given_speed_chat_when_translating_then_setspeed_command_carries_level(
    sleeper, chat, level, ac_id
):
    """Given each speed phrase, When translated, Then command=setSpeed with that level."""
    # Given
    client = ScriptedModelClient('{"command":"setSpeed","speed":"' + level + '"}')
    # When
    command = await translate(client, sleeper, chat)
    # Then
    assert command.command is CommandType.SET_SPEED, ac_id
    assert command.speed is SpeedLevel(level), ac_id
    assert command.color is None


@pytest.mark.parametrize(
    ("level", "ac_id"),
    [("low", "AC1.2.1"), ("medium", "AC1.2.2"), ("high", "AC1.2.3")],
)
async def test_given_setspeed_when_a_later_movement_is_translated_then_movement_uses_level(
    sleeper, level, ac_id
):
    """Given a prior setSpeed, When movement is translated, Then it carries that level (AC1.2.x)."""
    # Given — the movement reply deliberately omits speed; the old code defaulted
    # it to medium, which is the regression this scenario guards against.
    client = ScriptedModelClient(
        '{"command":"setSpeed","speed":"' + level + '"}',
        '{"command":"forward"}',
    )
    agent = make_agent(client, sleeper)
    await agent.translate(f"set speed {level}", CommandSource.CHAT)
    # When
    movement = await agent.translate("roll forward", CommandSource.CHAT)
    # Then
    assert movement.command is CommandType.FORWARD, ac_id
    assert movement.speed is SpeedLevel(level), ac_id
    assert movement.color is None


async def test_given_no_setspeed_when_movement_is_translated_then_medium_default_applies(sleeper):
    """Given no setSpeed has been seen, When movement is translated, Then medium is the default."""
    # Given
    client = ScriptedModelClient('{"command":"forward"}')
    agent = make_agent(client, sleeper)
    # When
    movement = await agent.translate("roll forward")
    # Then
    assert movement.speed is SpeedLevel.MEDIUM


async def test_given_two_speeds_when_movement_is_translated_then_latest_one_wins(sleeper):
    """Given a changed speed, When movement is translated, Then the latest level governs it."""
    # Given — the model suggests a stale "medium" for the movement; the
    # configured high level must be authoritative.
    client = ScriptedModelClient(
        '{"command":"setSpeed","speed":"low"}',
        '{"command":"setSpeed","speed":"high"}',
        '{"command":"forward","speed":"medium"}',
    )
    agent = make_agent(client, sleeper)
    await agent.translate("set speed low")
    await agent.translate("set speed high")
    # When
    movement = await agent.translate("roll forward")
    # Then
    assert movement.speed is SpeedLevel.HIGH


async def test_given_configured_speed_when_prompt_is_built_then_model_sees_active_level(sleeper):
    """Given a configured speed, When translating again, Then the active level is in the prompt."""
    # Given
    client = ScriptedModelClient(
        '{"command":"setSpeed","speed":"low"}',
        '{"command":"forward"}',
    )
    agent = make_agent(client, sleeper)
    await agent.translate("set speed low")
    # When
    await agent.translate("roll forward")
    # Then
    assert "Active robot speed: low" in client.calls[1][1]


async def test_given_setspeed_without_speed_when_translating_then_rephrase_error_is_raised(sleeper):
    """Given setSpeed with no speed value, When translated, Then the model output is rejected."""
    # Given
    client = ScriptedModelClient('{"command":"setSpeed"}')
    # When / Then
    with pytest.raises(AgentCommandError, match="rephrase"):
        await translate(client, sleeper, "set speed")


async def test_given_invalid_speed_value_when_translating_then_rephrase_error_is_raised(sleeper):
    """Given a speed outside low/medium/high, When translated, Then it is rejected."""
    # Given
    client = ScriptedModelClient('{"command":"setSpeed","speed":"turbo"}')
    # When / Then
    with pytest.raises(AgentCommandError, match="rephrase"):
        await translate(client, sleeper, "set speed turbo")
