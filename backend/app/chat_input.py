"""Chat input validation and forwarding to the agent translator.

This module owns the untrusted-input boundary (BR1.1 / NFR9.1). It never talks to
an LLM or to Bluetooth directly: the translator is injected, so the whole module
is testable offline.
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timezone
from typing import Protocol

from .config import DEFAULT_MAX_CHAT_LENGTH, configure_logging, log_event
from .models import ChatMessage, CommandSource, RobotCommand

_REPHRASE_HINT = "Please rephrase your command."

# Recognises the movement, speed and colour phrasings accepted by this MVP.
# Free-form within a phrase is fine ("roll forward", "please turn left"), but a
# message with no recognised intent is rejected before any robot action (BR1.1).
_COMMAND_PATTERN = re.compile(
    r"\b(?:forward|backwards?|back|left|right|stop|halt)\b"
    r"|\bset\s+(?:the\s+)?speed\s+(?:to\s+)?(?:low|medium|high)\b"
    r"|\bset\s+(?:the\s+)?(?:led\s+)?colou?r\s+(?:to\s+)?(?:red|blue|green)\b"
    r"|\b(?:change|switch)\s+(?:the\s+)?(?:led\s+)?colou?r\s+(?:to\s+)?(?:red|blue|green)\b",
    re.IGNORECASE,
)


class ChatInputError(ValueError):
    """A chat message failed validation. ``code`` is the chat-UI error type."""

    def __init__(self, message: str, code: str = "validation") -> None:
        super().__init__(message)
        self.code = code

    def to_chat_error(self) -> dict[str, str]:
        """Return the plain-language error payload the chat UI renders (BR1.3)."""
        return {
            "type": self.code,
            "message": str(self),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class AgentTranslator(Protocol):
    """Injected boundary for chat-to-command translation (implemented by AgentCommand)."""

    async def translate(
        self, text: str, source: CommandSource = CommandSource.CHAT
    ) -> RobotCommand: ...


class ChatInput:
    """Validate chat text, record the message, and forward it to the translator."""

    def __init__(
        self,
        agent: AgentTranslator,
        max_length: int = DEFAULT_MAX_CHAT_LENGTH,
        logger=None,
    ) -> None:
        self._agent = agent
        self._max_length = max_length
        self._logger = logger or configure_logging()

    def _decode(self, value: str | bytes) -> str:
        """Decode at the boundary; reject invalid UTF-8 and lone surrogates."""
        if isinstance(value, bytes):
            try:
                return value.decode("utf-8", errors="strict")
            except UnicodeDecodeError as exc:
                raise ChatInputError(f"That message was not valid UTF-8. {_REPHRASE_HINT}") from exc
        if not isinstance(value, str):
            raise ChatInputError(f"Chat input must be text. {_REPHRASE_HINT}")
        try:
            value.encode("utf-8", errors="strict")
        except UnicodeEncodeError as exc:
            raise ChatInputError(f"That message was not valid UTF-8. {_REPHRASE_HINT}") from exc
        return value

    def validate(self, value: str | bytes) -> str:
        """Return normalised text or raise :class:`ChatInputError`."""
        text = self._decode(value).strip()
        if not text:
            raise ChatInputError(f"Please type a message to control the robot. {_REPHRASE_HINT}")
        if len(text) > self._max_length:
            raise ChatInputError(
                f"That message is too long ({len(text)} characters, limit {self._max_length}). "
                f"Please shorten it and rephrase."
            )
        if _COMMAND_PATTERN.search(text) is None:
            raise ChatInputError(
                f"I did not recognise a robot command in that message. {_REPHRASE_HINT}"
            )
        return text

    async def handle(
        self, value: str | bytes, source: CommandSource = CommandSource.CHAT
    ) -> RobotCommand:
        """Validate and forward a chat message, returning the translated command."""
        started = time.monotonic()
        text = self.validate(value)
        message = ChatMessage(text=text)
        log_event(
            self._logger,
            "chat_received",
            message_id=message.message_id,
            source=source.value,
            text_length=len(text),
        )
        command = await self._agent.translate(text, source)
        log_event(
            self._logger,
            "chat_forwarded",
            message_id=message.message_id,
            command_id=command.command_id,
            command=command.command.value,
            duration_ms=round((time.monotonic() - started) * 1000, 2),
        )
        return command
