"""Chat-to-command translation via LangChain Deep Agents + OpenRouter.

The language model sits behind the :class:`ModelClient` protocol. Production uses
:class:`DeepAgentsModelClient`, whose third-party imports are lazy; tests inject a
scripted client and need no API key, network access, or Deep Agents install.
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timezone
from typing import Any, Protocol

from .config import (
    DEFAULT_COMMAND_TIMEOUT_S,
    DEFAULT_OPENROUTER_BASE_URL,
    DEFAULT_OPENROUTER_MODEL,
    DEFAULT_RETRY_BASE_DELAY_S,
    DEFAULT_RETRY_MAX_DELAY_S,
    configure_logging,
    log_event,
)
from .models import (
    MOVEMENT_COMMANDS,
    ColorValue,
    CommandSource,
    CommandType,
    RobotCommand,
    SpeedLevel,
)

SYSTEM_PROMPT = """You translate a natural-language request into exactly ONE Sphero Mini command.
Reply with ONLY a JSON object. No prose, no markdown fences.
Fields:
- command: one of forward, back, left, right, stop, setSpeed, setColor
- speed: one of low, medium, high (required for setSpeed; optional for movement)
- color: one of red, blue, green (required for setColor)
An earlier "set speed" message sets the active speed, which is supplied in the
user message; a later movement command must use it even if omitted here.
Examples:
"roll forward" -> {"command":"forward","speed":"medium"}
"set speed low" -> {"command":"setSpeed","speed":"low"}
"set color red" -> {"command":"setColor","color":"red"}
If the request is unclear or no command can be determined, reply {"command":null}.
"""


class ModelClientError(RuntimeError):
    """The real model client could not be constructed or reached its dependency."""


class AgentCommandError(RuntimeError):
    """Translation failed; the message is safe to show in the chat UI (BR1.3)."""

    def __init__(self, message: str, code: str = "agent_error") -> None:
        super().__init__(message)
        self.code = code

    def to_chat_error(self) -> dict[str, str]:
        return {
            "type": self.code,
            "message": str(self),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class ModelClient(Protocol):
    """Injected LLM boundary: one completion per translation attempt."""

    async def complete(self, system: str, user: str) -> str: ...


def _load_chat_model_class():
    """Import the OpenRouter-compatible chat model lazily (never at module import)."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ModelClientError(
            "langchain-openai is required for live chat translation. "
            "Install the runtime dependencies from requirements.txt."
        ) from exc
    return ChatOpenAI


def _load_deep_agent_factory():
    """Return Deep Agents' factory when installed, otherwise ``None`` (direct LLM fallback)."""
    try:
        from deepagents import create_deep_agent
    except ImportError:
        return None
    return create_deep_agent


def _extract_text(result: Any) -> str:
    """Normalise LangChain/Deep Agents response shapes to a single string."""
    if isinstance(result, str):
        return result
    content = getattr(result, "content", None)
    if content is None and isinstance(result, dict):
        for message in reversed(result.get("messages", [])):
            candidate = (
                message.get("content")
                if isinstance(message, dict)
                else getattr(message, "content", None)
            )
            if candidate:
                content = candidate
                break
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict):
                parts.append(str(part.get("text", "")))
            else:
                parts.append(str(getattr(part, "text", part)))
        content = "".join(parts)
    return content if isinstance(content, str) else (str(content) if content is not None else "")


class DeepAgentsModelClient:
    """Production model client: Deep Agents harness (when present) over OpenRouter.

    The API key is held on the instance only and is never logged or returned in
    error messages.
    """

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_OPENROUTER_MODEL,
        base_url: str = DEFAULT_OPENROUTER_BASE_URL,
        timeout_s: float = DEFAULT_COMMAND_TIMEOUT_S,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._base_url = base_url
        self._timeout_s = timeout_s

    async def complete(self, system: str, user: str) -> str:
        chat_model_class = _load_chat_model_class()
        llm = chat_model_class(
            model=self._model,
            api_key=self._api_key,
            base_url=self._base_url,
            temperature=0,
            timeout=self._timeout_s,
        )
        factory = _load_deep_agent_factory()
        if factory is not None:
            agent = factory(model=llm, system_prompt=system, tools=[])
            return _extract_text(
                await agent.ainvoke({"messages": [{"role": "user", "content": user}]})
            )
        return _extract_text(
            await llm.ainvoke(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ]
            )
        )


def _parse_payload(content: str) -> dict[str, Any]:
    """Extract a JSON object from a model reply, tolerating markdown fences."""
    text = content.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.lower().startswith("json"):
            text = text[4:]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise AgentCommandError(
            "I could not turn that message into a robot command. Please rephrase."
        )
    try:
        payload = json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise AgentCommandError(
            "I could not understand the command response. Please rephrase."
        ) from exc
    if not isinstance(payload, dict):
        raise AgentCommandError("That command was not valid. Please rephrase.")
    return payload


class AgentCommand:
    """Translate validated chat text into a single validated :class:`RobotCommand`."""

    def __init__(
        self,
        client: ModelClient,
        sleeper=None,
        max_attempts: int = 2,
        retry_base_delay_s: float = DEFAULT_RETRY_BASE_DELAY_S,
        retry_max_delay_s: float = DEFAULT_RETRY_MAX_DELAY_S,
        logger=None,
        default_speed: SpeedLevel = SpeedLevel.MEDIUM,
    ) -> None:
        self._client = client
        self._sleeper = sleeper or asyncio.sleep
        self._max_attempts = max_attempts
        self._retry_base_delay_s = retry_base_delay_s
        self._retry_max_delay_s = retry_max_delay_s
        self._logger = logger or configure_logging()
        self._default_speed = default_speed
        # FR1.2 / AC1.2.1–AC1.2.3: the last setSpeed level governs every later
        # movement command until a different setSpeed is translated. This instance
        # is the single translation boundary in the chat pipeline, so the state
        # persists across messages on the socket and across one-shot sockets.
        self._configured_speed: SpeedLevel | None = None

    async def _call_model(self, user_prompt: str) -> str:
        """Call the injected model client, retrying once with bounded backoff."""
        last_error: Exception | None = None
        for attempt in range(1, self._max_attempts + 1):
            try:
                return await self._client.complete(SYSTEM_PROMPT, user_prompt)
            except Exception as exc:  # external boundary: client SDKs raise varied errors
                last_error = exc
                log_event(
                    self._logger,
                    "agent_translation_failed",
                    attempt=attempt,
                    error_type=type(exc).__name__,
                )
                if attempt < self._max_attempts:
                    delay = min(
                        self._retry_base_delay_s * (2 ** (attempt - 1)),
                        self._retry_max_delay_s,
                    )
                    log_event(self._logger, "agent_retry", attempt=attempt, delay_s=delay)
                    await self._sleeper(delay)
        raise AgentCommandError(
            "The language service is unavailable right now. Please try again."
        ) from last_error

    async def translate(
        self, text: str, source: CommandSource = CommandSource.CHAT
    ) -> RobotCommand:
        """Translate free-form chat into one allowed robot command."""
        started = time.monotonic()
        # Give the model the active speed so its reply is consistent with the
        # level we enforce below; the level itself is applied deterministically.
        speed_context = (
            f"Active robot speed: {self._configured_speed.value}.\n"
            if self._configured_speed is not None
            else ""
        )
        content = await self._call_model(f"{speed_context}User message: {text!r}")
        payload = _parse_payload(content)
        raw_command = payload.get("command")
        if not isinstance(raw_command, str):
            raise AgentCommandError("I did not understand that. Please rephrase.")
        try:
            command_type = CommandType(raw_command)
        except ValueError as exc:
            raise AgentCommandError(
                f"'{raw_command}' is not a command I can run. Please rephrase."
            ) from exc

        fields: dict[str, Any] = {"command": command_type, "source": source}
        if command_type in MOVEMENT_COMMANDS:
            if self._configured_speed is not None:
                # A configured speed is authoritative for later movement — never
                # overwrite it with the model's stale/default "medium" value.
                fields["speed"] = self._configured_speed
            else:
                fields["speed"] = self._enum_field(
                    payload.get("speed") or self._default_speed.value, SpeedLevel, "speed"
                )
        elif command_type is CommandType.SET_SPEED:
            configured = self._enum_field(payload.get("speed"), SpeedLevel, "speed")
            fields["speed"] = configured
            self._configured_speed = configured
            log_event(self._logger, "speed_configured", speed=configured.value)
        elif command_type is CommandType.SET_COLOR:
            fields["color"] = self._enum_field(payload.get("color"), ColorValue, "color")

        command = RobotCommand(**fields)
        log_event(
            self._logger,
            "command_emitted",
            command_id=command.command_id,
            command=command.command.value,
            duration_ms=round((time.monotonic() - started) * 1000, 2),
        )
        return command

    @staticmethod
    def _enum_field(value: Any, enum_type, field_name: str):
        """Validate an enum payload field, mapping bad values to a rephrase request."""
        try:
            return enum_type(value)
        except (ValueError, TypeError) as exc:
            raise AgentCommandError(
                f"That {field_name} is not supported. Please rephrase."
            ) from exc
