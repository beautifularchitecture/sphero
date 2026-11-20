"""Walking-skeleton scenario for U1: chat frame → agent translation → BLE write → ack.

Uses scripted offline doubles only: no OpenRouter key, network, robot or BLE
adapter is required. U2/U3's stats-rendering skeleton is verified in their own
units; this scenario verifies the U1 slice end to end.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

from fastapi import WebSocketDisconnect

from backend.app.agent_command import AgentCommand
from backend.app.chat_input import ChatInput
from backend.app.main import handle_chat_websocket
from backend.app.models import CommandExecutionStatus
from backend.app.robot_command import BleConnectionError, RobotCommandSender


class ScriptedModelClient:
    def __init__(self, *responses: str) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[str, str]] = []

    async def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        return self.responses.pop(0)


class RecordingSleeper:
    def __init__(self) -> None:
        self.delays: list[float] = []

    async def __call__(self, delay: float) -> None:
        self.delays.append(delay)


class FakeBle:
    def __init__(self, *, fail_writes: bool = False) -> None:
        self.connected = True
        self.fail_writes = fail_writes
        self.writes: list[tuple[str, str, bytes]] = []

    async def connect(self) -> None:
        self.connected = True

    async def is_connected(self) -> bool:
        return self.connected

    async def write_gatt(self, service: str, characteristic: str, payload: bytes) -> None:
        self.writes.append((service, characteristic, payload))
        if self.fail_writes:
            self.connected = False
            raise BleConnectionError("robot disconnected mid-write")

    async def disconnect(self) -> None:
        self.connected = False


class FakeWebSocket:
    def __init__(self, *frames: str) -> None:
        self.incoming = list(frames)
        self.sent: list[str] = []
        self.accepted = False

    async def accept(self) -> None:
        self.accepted = True

    async def receive_text(self) -> str:
        if not self.incoming:
            raise WebSocketDisconnect(code=1000)
        return self.incoming.pop(0)

    async def send_text(self, payload: str) -> None:
        self.sent.append(payload)


def make_skeleton(
    model: ScriptedModelClient,
    statuses: list[CommandExecutionStatus],
    ble: FakeBle | None = None,
):
    sleeper = RecordingSleeper()
    ble = ble or FakeBle()
    agent = AgentCommand(client=model, sleeper=sleeper)  # type: ignore[arg-type]
    sender = RobotCommandSender(
        ble_client=ble,  # type: ignore[arg-type]
        status_callback=statuses.append,
        sleeper=sleeper,  # type: ignore[arg-type]
    )
    pipeline = SimpleNamespace(chat_input=ChatInput(agent=agent), sender=sender)
    return pipeline, ble, model, sleeper


async def test_given_scripted_chat_when_the_full_skeleton_runs_then_a_ble_write_ack_and_status_are_produced():
    """Given a valid chat frame, When chat→agent→BLE runs, Then all boundaries fire."""
    # Given
    model = ScriptedModelClient(json.dumps({"command": "forward", "speed": "medium"}))
    statuses: list[CommandExecutionStatus] = []
    pipeline, ble, model, sleeper = make_skeleton(model, statuses)
    socket = FakeWebSocket('{"text":"roll forward"}')

    # When
    await handle_chat_websocket(socket, pipeline)  # type: ignore[arg-type]

    # Then
    assert socket.accepted is True
    assert len(model.calls) == 1
    assert "roll forward" in model.calls[0][1]
    assert len(ble.writes) == 1
    written: dict[str, Any] = json.loads(ble.writes[0][2].decode("utf-8"))
    assert written["command"] == "forward"
    assert written["speed"] == "medium"
    assert len(statuses) == 1
    assert statuses[0].command_id == written["commandId"]
    assert statuses[0].status.value == "moving"
    ack = json.loads(socket.sent[0])
    assert ack["type"] == "ack"
    assert ack["status"] == "moving"
    assert ack["commandId"] == written["commandId"]
    assert sleeper.delays == []


async def test_given_agent_uncertainty_when_the_full_skeleton_runs_then_stop_is_written_and_error_is_shown():
    """Given an unsupported model reply, When handled, Then a STOP is written and an error is shown (BR1.3)."""
    # Given
    # The chat text passes input validation, but the model returns an unsupported
    # command — this exercises the agent boundary's rephrase error, not BR1.1.
    model = ScriptedModelClient(json.dumps({"command": "dance"}))
    statuses: list[CommandExecutionStatus] = []
    pipeline, ble, _model, _sleeper = make_skeleton(model, statuses)
    socket = FakeWebSocket('{"text":"roll forward"}')

    # When
    await handle_chat_websocket(socket, pipeline)  # type: ignore[arg-type]

    # Then — no movement was sent, but the safety stop is (BR1.3 / AC1.5.2).
    assert len(ble.writes) == 1
    stopped = json.loads(ble.writes[0][2].decode("utf-8"))
    assert stopped["command"] == "stop"
    assert len(statuses) == 1
    assert statuses[0].status.value == "stopped"
    error = json.loads(socket.sent[0])
    assert error["type"] == "error"
    assert error["errorType"] == "agent_error"
    assert "rephrase" in error["message"].lower()


async def test_given_ble_disconnect_when_the_full_skeleton_runs_then_stop_is_attempted_and_error_is_shown():
    """Given a robot disconnect mid-command, When handled, Then a STOP is attempted and an error is shown (AC1.5.4)."""
    # Given
    model = ScriptedModelClient(json.dumps({"command": "forward", "speed": "medium"}))
    statuses: list[CommandExecutionStatus] = []
    ble = FakeBle(fail_writes=True)
    pipeline, ble, _model, _sleeper = make_skeleton(model, statuses, ble=ble)
    socket = FakeWebSocket('{"text":"roll forward"}')

    # When
    await handle_chat_websocket(socket, pipeline)  # type: ignore[arg-type]

    # Then — the sender retried the movement and then tried to stop the robot.
    commands = [json.loads(write[2].decode("utf-8"))["command"] for write in ble.writes]
    assert "forward" in commands
    assert "stop" in commands
    error = json.loads(socket.sent[0])
    assert error["type"] == "error"
    assert error["errorType"] == "bluetooth"


async def test_given_configured_speed_when_a_later_movement_runs_then_ble_payload_uses_it():
    """Given setSpeed then movement, When the skeleton runs, Then the BLE payload carries the set speed (AC1.2.x)."""
    # Given — the movement reply deliberately omits speed: the pipeline must
    # carry the earlier configured level end to end (the empirical R-06 probe).
    model = ScriptedModelClient(
        json.dumps({"command": "setSpeed", "speed": "low"}),
        json.dumps({"command": "forward"}),
    )
    statuses: list[CommandExecutionStatus] = []
    pipeline, ble, _model, _sleeper = make_skeleton(model, statuses)
    socket = FakeWebSocket('{"text":"set speed low"}', '{"text":"roll forward"}')

    # When
    await handle_chat_websocket(socket, pipeline)  # type: ignore[arg-type]

    # Then
    assert len(ble.writes) == 2
    movement = json.loads(ble.writes[1][2].decode("utf-8"))
    assert movement["command"] == "forward"
    assert movement["speed"] == "low"
    assert len(socket.sent) == 2
    assert json.loads(socket.sent[1])["type"] == "ack"
