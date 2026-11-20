"""Pydantic domain models for chat messages and robot commands.

Shapes follow the U1 entity model and Contract 1 (CommandExecutionStatus).
All enums derive from ``str`` so models serialise to plain JSON-friendly values.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator, model_validator


class CommandType(str, Enum):
    """Allowed robot-command vocabulary (BR1.2)."""

    FORWARD = "forward"
    BACK = "back"
    LEFT = "left"
    RIGHT = "right"
    STOP = "stop"
    SET_SPEED = "setSpeed"
    SET_COLOR = "setColor"


MOVEMENT_COMMANDS = frozenset(
    {
        CommandType.FORWARD,
        CommandType.BACK,
        CommandType.LEFT,
        CommandType.RIGHT,
    }
)


class SpeedLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ColorValue(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"


class CommandStatus(str, Enum):
    MOVING = "moving"
    STOPPED = "stopped"
    ERROR = "error"


class CommandSource(str, Enum):
    CHAT = "chat"
    BUTTON = "button"
    API = "api"


class MessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class MessageSender(str, Enum):
    USER = "user"
    AGENT = "agent"


class MessageType(str, Enum):
    COMMAND = "command"
    QUERY = "query"
    STATUS = "status"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex}"


class ChatMessage(BaseModel):
    """A chat message entering or leaving the chat window."""

    message_id: str = Field(default_factory=lambda: _new_id("msg"))
    text: str
    timestamp: datetime = Field(default_factory=_utc_now)
    direction: MessageDirection = MessageDirection.INBOUND
    sender: MessageSender = MessageSender.USER
    message_type: MessageType = MessageType.COMMAND
    language: str | None = None

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        """Reject empty and whitespace-only text at the boundary (BR1.1, NFR9.1)."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("chat text must not be empty or whitespace-only")
        return stripped


class RobotCommand(BaseModel):
    """A validated command ready to be sent to the Sphero Mini over BLE."""

    command_id: str = Field(default_factory=lambda: _new_id("cmd"))
    command: CommandType
    speed: SpeedLevel | None = None
    color: ColorValue | None = None
    timestamp: datetime = Field(default_factory=_utc_now)
    status: CommandStatus = CommandStatus.STOPPED
    source: CommandSource = CommandSource.CHAT
    retry_count: int = Field(default=0, ge=0)

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    @model_validator(mode="after")
    def required_payload_for_parameterised_commands(self) -> RobotCommand:
        """setColor needs a color and setSpeed needs a speed (entity constraints)."""
        if self.command is CommandType.SET_COLOR and self.color is None:
            raise ValueError("setColor requires a color")
        if self.command is CommandType.SET_SPEED and self.speed is None:
            raise ValueError("setSpeed requires a speed")
        return self


class CommandExecutionStatus(BaseModel):
    """Contract 1 payload reported from U1 to U2 via sync callback."""

    command_id: str = Field(
        validation_alias=AliasChoices("command_id", "commandId"),
        serialization_alias="commandId",
    )
    status: CommandStatus
    timestamp: str = Field(default_factory=lambda: _utc_now().isoformat())

    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)
