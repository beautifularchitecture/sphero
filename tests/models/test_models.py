"""BDD scenarios for the chat and robot command domain models (BR1.1, BR1.2, Contract 1)."""

from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from backend.app.models import (
    ChatMessage,
    CommandExecutionStatus,
    CommandSource,
    CommandStatus,
    CommandType,
    RobotCommand,
)


def test_given_valid_chat_text_when_creating_chat_message_then_defaults_are_applied():
    """Given valid chat text, When a ChatMessage is created, Then direction/sender/type default."""
    # Given / When
    message = ChatMessage(text="roll forward")
    # Then
    assert message.text == "roll forward"
    assert message.direction == "inbound"
    assert message.sender == "user"
    assert message.message_type == "command"
    assert message.message_id
    assert isinstance(message.timestamp, datetime)


@pytest.mark.parametrize("bad_text", ["", "   ", "\n\t"])
def test_given_empty_or_whitespace_chat_text_when_creating_message_then_validation_fails(
    bad_text,
):
    """Given empty or whitespace-only text (BR1.1), When created, Then validation fails."""
    with pytest.raises(ValidationError):
        ChatMessage(text=bad_text)


def test_given_invalid_message_type_when_creating_chat_message_then_validation_fails():
    """Given a message type outside command/query/status, When created, Then validation fails."""
    with pytest.raises(ValidationError):
        ChatMessage(text="roll forward", message_type="unknown")  # type: ignore[arg-type]


def test_given_movement_command_when_creating_robot_command_then_speed_is_accepted():
    """Given a movement command with a speed, When created, Then the command is valid."""
    # Given / When
    command = RobotCommand(command=CommandType.FORWARD, speed="medium", source=CommandSource.CHAT)
    # Then
    assert command.command == CommandType.FORWARD
    assert command.speed == "medium"
    assert command.retry_count == 0
    assert command.status == CommandStatus.STOPPED


def test_given_set_color_command_without_color_when_creating_command_then_validation_fails():
    """Given setColor without a color (entities constraint), When created, Then validation fails."""
    with pytest.raises(ValidationError, match="color"):
        RobotCommand(command=CommandType.SET_COLOR, source=CommandSource.CHAT)


def test_given_unknown_robot_command_when_creating_command_then_validation_fails():
    """Given a command outside the allowed vocabulary (BR1.2), When created, Then validation fails."""
    with pytest.raises(ValidationError):
        RobotCommand(command="dance", source=CommandSource.CHAT)  # type: ignore[arg-type]


def test_given_executed_command_when_creating_status_then_contract_fields_are_serializable():
    """Given a command status, When serialized, Then Contract 1's fields are present."""
    # Given / When
    status = CommandExecutionStatus(
        command_id="cmd-123", status=CommandStatus.MOVING, timestamp="2026-11-19T10:00:00Z"
    )
    payload = status.model_dump(mode="json")
    # Then
    assert payload == {
        "commandId": "cmd-123",
        "status": "moving",
        "timestamp": "2026-11-19T10:00:00Z",
    }


def test_given_invalid_execution_status_when_creating_status_then_validation_fails():
    """Given a status outside moving/stopped/error, When created, Then validation fails."""
    with pytest.raises(ValidationError):
        CommandExecutionStatus(
            command_id="cmd-123", status="unknown", timestamp="2026-11-19T10:00:00Z"
        )
