"""BDD scenarios for chat→command translation (FR1.1, BR1.2, BR1.3, NFR4.3).

All scenarios inject a scripted model client: no OpenRouter key, network, or
physical robot is needed. The real adapter's lazy-import boundary is exercised
separately with monkeypatched import helpers.
"""

from __future__ import annotations

import asyncio
import json
import sys

import pytest

from backend.app import agent_command as agent_module
from backend.app.agent_command import (
    AgentCommandError,
    DeepAgentsModelClient,
    ModelClientError,
)
from backend.app.models import CommandSource, CommandType, SpeedLevel

from .conftest import RecordingSleeper, ScriptedModelClient, make_agent, translate


async def test_given_plain_json_response_when_translating_then_forward_command_is_emitted(sleeper):
    """Given the model returns a valid command, When translating, Then a RobotCommand is built."""
    # Given
    client = ScriptedModelClient('{"command":"forward","speed":"medium"}')
    # When
    command = await translate(client, sleeper, "roll forward")
    # Then
    assert command.command is CommandType.FORWARD
    assert command.speed is SpeedLevel.MEDIUM
    assert command.source is CommandSource.CHAT
    assert sleeper.delays == []


async def test_given_json_fenced_response_when_translating_then_command_is_still_parsed(sleeper):
    """Given a fenced response, When translating, Then the JSON payload is extracted."""
    # Given
    client = ScriptedModelClient('```json\n{"command":"right","speed":"high"}\n```')
    # When
    command = await translate(client, sleeper, "turn right")
    # Then
    assert command.command is CommandType.RIGHT
    assert command.speed is SpeedLevel.HIGH


async def test_given_freeform_phrasing_when_translating_then_left_command_is_emitted(sleeper):
    """Given a natural-language left request, When translating, Then the vocabulary maps to left."""
    # Given
    client = ScriptedModelClient('{"command":"left","speed":"low"}')
    # When
    command = await translate(client, sleeper, "please go left towards the door")
    # Then
    assert command.command is CommandType.LEFT
    assert "please go left" in client.calls[0][1]


async def test_given_stop_response_when_translating_then_no_speed_is_required(sleeper):
    """Given a stop command, When translating, Then no speed payload is attached."""
    # Given
    client = ScriptedModelClient('{"command":"stop"}')
    # When
    command = await translate(client, sleeper, "stop")
    # Then
    assert command.command is CommandType.STOP
    assert command.speed is None


async def test_given_uncertain_model_response_when_translating_then_rephrase_error_is_raised(
    sleeper,
):
    """Given the model is unsure (FR3), When translating, Then no robot command is emitted."""
    # Given
    client = ScriptedModelClient('{"command":null}')
    # When / Then
    with pytest.raises(AgentCommandError, match="rephrase"):
        await translate(client, sleeper, "do something interesting")


async def test_given_malformed_json_when_translating_then_rephrase_error_is_raised(sleeper):
    """Given unparseable model output, When translating, Then a plain-language error is raised."""
    # Given
    client = ScriptedModelClient("I am not sure what you mean")
    # When / Then
    with pytest.raises(AgentCommandError, match="rephrase"):
        await translate(client, sleeper, "dance")


async def test_given_unknown_command_value_when_translating_then_rephrase_error_is_raised(sleeper):
    """Given a command outside the allowed vocabulary (BR1.2), When translating, Then it is rejected."""
    # Given
    client = ScriptedModelClient('{"command":"fly","speed":"medium"}')
    # When / Then
    with pytest.raises(AgentCommandError, match="rephrase"):
        await translate(client, sleeper, "fly to the moon")


async def test_given_model_fails_once_when_translating_then_one_retry_succeeds(sleeper):
    """Given a transient model error, When translating, Then one backoff retry succeeds."""
    # Given
    client = ScriptedModelClient(RuntimeError("timeout"), '{"command":"forward","speed":"medium"}')
    # When
    command = await translate(client, sleeper, "roll forward")
    # Then
    assert command.command is CommandType.FORWARD
    assert len(client.calls) == 2
    assert sleeper.delays == pytest.approx([0.1])


async def test_given_model_fails_twice_when_translating_then_agent_error_is_surfaced(sleeper):
    """Given persistent model failure (FR4), When translating, Then the error reaches the chat UI."""
    # Given
    client = ScriptedModelClient(RuntimeError("timeout"), RuntimeError("timeout"))
    # When / Then
    with pytest.raises(AgentCommandError, match="unavailable"):
        await translate(client, sleeper, "roll forward")
    assert len(client.calls) == 2
    assert sleeper.delays == pytest.approx([0.1])


async def test_given_model_failure_when_converted_to_chat_error_then_type_is_agent_error():
    """Given an agent failure, When converted for the UI, Then it is typed as agent_error."""
    error = AgentCommandError("language service unavailable")
    assert error.to_chat_error()["type"] == "agent_error"
    assert error.to_chat_error()["timestamp"]


def test_given_missing_runtime_package_when_building_real_client_then_error_names_dependency(
    monkeypatch,
):
    """Given langchain-openai is absent, When the real client runs, Then it fails loudly."""
    # Given — a module set to None makes the real lazy import raise ImportError
    monkeypatch.setitem(sys.modules, "langchain_openai", None)
    client = DeepAgentsModelClient(api_key="sk-or-secret-value", model="test-model")
    # When / Then
    with pytest.raises(ModelClientError, match="langchain-openai"):
        asyncio.run(client.complete("system", "user"))


def test_given_deep_agents_available_when_real_client_completes_then_agent_result_is_used(
    monkeypatch,
):
    """Given the Deep Agents harness is installed, When completing, Then its output is returned."""
    # Given
    recorded: dict[str, object] = {}

    class FakeLlm:
        def __init__(self, **kwargs) -> None:
            recorded["llm_kwargs"] = kwargs

    class FakeAgent:
        async def ainvoke(self, payload):
            recorded["agent_payload"] = payload
            return {"messages": [{"role": "assistant", "content": '{"command":"forward"}'}]}

    def fake_factory(**kwargs):
        recorded["factory_kwargs"] = kwargs
        return FakeAgent()

    monkeypatch.setattr(agent_module, "_load_chat_model_class", lambda: FakeLlm)
    monkeypatch.setattr(agent_module, "_load_deep_agent_factory", lambda: fake_factory)
    client = DeepAgentsModelClient(api_key="sk-or-secret-value", model="test-model")
    # When
    result = asyncio.run(client.complete("system prompt", "user text"))
    # Then
    assert json.loads(result) == {"command": "forward"}
    assert recorded["llm_kwargs"]["api_key"] == "sk-or-secret-value"
    assert recorded["agent_payload"] == {"messages": [{"role": "user", "content": "user text"}]}


def test_given_deep_agents_absent_when_real_client_completes_then_chat_model_is_used(
    monkeypatch,
):
    """Given no Deep Agents harness, When completing, Then the pinned chat model is called directly."""
    # Given
    class FakeLlm:
        def __init__(self, **kwargs) -> None:
            self.kwargs = kwargs

        async def ainvoke(self, messages):
            return type("Response", (), {"content": '{"command":"stop"}'})()

    monkeypatch.setattr(agent_module, "_load_chat_model_class", lambda: FakeLlm)
    monkeypatch.setattr(agent_module, "_load_deep_agent_factory", lambda: None)
    client = DeepAgentsModelClient(api_key="sk-or-secret-value", model="test-model")
    # When
    result = asyncio.run(client.complete("system prompt", "user text"))
    # Then
    assert json.loads(result) == {"command": "stop"}
