"""BDD scenarios for chat input validation and forwarding (AC1.1.1–AC1.1.5, BR1.1, NFR9.1).

The agent is an injected fake: validation is tested in isolation, with no LLM and
no robot. These scenarios are written before the implementation they specify.
"""

from __future__ import annotations

import pytest

from backend.app.chat_input import ChatInput, ChatInputError
from backend.app.models import CommandSource, CommandType, RobotCommand, SpeedLevel


class FakeAgent:
    """Records translations; returns a deterministic forward command."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, CommandSource]] = []

    async def translate(self, text: str, source: CommandSource = CommandSource.CHAT) -> RobotCommand:
        self.calls.append((text, source))
        return RobotCommand(command=CommandType.FORWARD, speed=SpeedLevel.MEDIUM, source=source)


def make_command() -> ChatInput:
    return ChatInput(agent=FakeAgent(), max_length=500)


@pytest.mark.parametrize(
    ("text", "ac_id"),
    [
        ("roll forward", "AC1.1.1"),
        ("stop", "AC1.1.2"),
        ("turn left", "AC1.1.3"),
        ("turn right", "AC1.1.4"),
        ("roll back", "AC1.1.5"),
    ],
)
async def test_given_known_movement_chat_when_handled_then_agent_receives_normalised_text(
    text, ac_id
):
    """Given each AC1.1 movement phrase, When handled, Then the agent translates it."""
    # Given
    agent = FakeAgent()
    chat_input = ChatInput(agent=agent, max_length=500)
    # When
    command = await chat_input.handle(text)
    # Then
    assert command.command is CommandType.FORWARD
    assert agent.calls == [(text, CommandSource.CHAT)], ac_id


async def test_given_valid_chat_when_handled_then_rephrase_error_is_not_raised():
    """Given a valid command phrase, When handled, Then forwarding succeeds cleanly."""
    # Given / When
    command = await make_command().handle("set speed low")
    # Then
    assert command.source is CommandSource.CHAT


@pytest.mark.parametrize("text", ["", "   ", "\n\t  "])
async def test_given_empty_or_whitespace_chat_when_handled_then_rephrase_error_is_raised(text):
    """Given empty or whitespace-only input, When handled, Then no agent call happens."""
    # Given
    agent = FakeAgent()
    chat_input = ChatInput(agent=agent, max_length=500)
    # When / Then
    with pytest.raises(ChatInputError, match="rephrase|type a message"):
        await chat_input.handle(text)
    assert agent.calls == []


async def test_given_invalid_utf8_bytes_when_handled_then_rephrase_error_is_raised():
    """Given invalid UTF-8 bytes at the boundary, When handled, Then the message is rejected."""
    # Given
    agent = FakeAgent()
    chat_input = ChatInput(agent=agent, max_length=500)
    # When / Then
    with pytest.raises(ChatInputError, match="UTF-8"):
        await chat_input.handle(b"\xff\xfe")
    assert agent.calls == []


async def test_given_unknown_command_when_handled_then_rephrase_error_is_raised():
    """Given an unrecognised phrase (BR1.1), When handled, Then no robot action is requested."""
    # Given
    agent = FakeAgent()
    chat_input = ChatInput(agent=agent, max_length=500)
    # When / Then
    with pytest.raises(ChatInputError, match="rephrase"):
        await chat_input.handle("dance a victory jig")
    assert agent.calls == []


async def test_given_overlong_chat_when_handled_then_rephrase_error_is_raised():
    """Given input longer than the configured limit, When handled, Then it is rejected."""
    # Given
    agent = FakeAgent()
    chat_input = ChatInput(agent=agent, max_length=20)
    # When / Then
    with pytest.raises(ChatInputError, match="too long"):
        await chat_input.handle("roll forward " * 5)
    assert agent.calls == []


async def test_given_rejected_chat_when_converted_to_error_report_then_plain_language_is_returned():
    """Given a validation failure, When converted for the chat UI, Then a typed error is produced."""
    # Given
    chat_input = make_command()
    # When
    with pytest.raises(ChatInputError) as caught:
        chat_input.validate("dance")
    report = caught.value.to_chat_error()
    # Then
    assert report["type"] == "validation"
    assert "rephrase" in report["message"].lower()
    assert report["timestamp"]


async def test_given_agent_failure_when_handled_then_the_error_propagates():
    """Given the agent cannot translate (FR4), When handled, Then the error reaches the caller."""

    class FailingAgent:
        async def translate(self, text, source=CommandSource.CHAT):
            raise RuntimeError("model unavailable")

    # Given
    chat_input = ChatInput(agent=FailingAgent(), max_length=500)  # type: ignore[arg-type]
    # When / Then
    with pytest.raises(RuntimeError, match="model unavailable"):
        await chat_input.handle("roll forward")
