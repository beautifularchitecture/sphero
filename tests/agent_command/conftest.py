"""Shared offline doubles for agent-translation scenarios."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

import pytest

from backend.app.agent_command import AgentCommand
from backend.app.models import CommandSource


class ScriptedModelClient:
    """Returns scripted responses or raises scripted exceptions, recording calls."""

    def __init__(self, *script: str | Exception) -> None:
        self.script = list(script)
        self.calls: list[tuple[str, str]] = []

    async def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class RecordingSleeper:
    """Captures backoff delays without actually sleeping."""

    def __init__(self) -> None:
        self.delays: list[float] = []

    async def __call__(self, delay: float) -> None:
        self.delays.append(delay)


@pytest.fixture
def sleeper() -> RecordingSleeper:
    return RecordingSleeper()


def make_agent(
    client: ScriptedModelClient,
    sleeper: RecordingSleeper,
    *,
    max_attempts: int = 2,
) -> AgentCommand:
    return AgentCommand(
        client=client,  # type: ignore[arg-type]
        sleeper=sleeper,  # type: ignore[arg-type]
        max_attempts=max_attempts,
        retry_base_delay_s=0.1,
        retry_max_delay_s=0.5,
    )


async def translate(client: ScriptedModelClient, sleeper: RecordingSleeper, text: str):
    return await make_agent(client, sleeper).translate(text, CommandSource.CHAT)
