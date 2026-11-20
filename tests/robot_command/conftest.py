"""Offline BLE doubles for command-execution scenarios."""

from __future__ import annotations

import pytest

from backend.app.robot_command import RobotCommandSender


class FakeBleClient:
    """In-memory BLE client; scripts connection/write failures without hardware."""

    def __init__(
        self,
        *,
        connected: bool = True,
        connect_errors: tuple[Exception, ...] = (),
        write_errors: tuple[Exception | None, ...] = (),
    ) -> None:
        self.connected = connected
        self.connect_errors = list(connect_errors)
        self.write_errors = list(write_errors)
        self.connect_calls = 0
        self.disconnect_calls = 0
        self.writes: list[tuple[str, str, bytes]] = []

    async def connect(self) -> None:
        self.connect_calls += 1
        if self.connect_errors:
            error = self.connect_errors.pop(0)
            if error is not None:
                raise error
        self.connected = True

    async def is_connected(self) -> bool:
        return self.connected

    async def write_gatt(self, service_uuid: str, characteristic_uuid: str, payload: bytes) -> None:
        self.writes.append((service_uuid, characteristic_uuid, payload))
        if self.write_errors:
            error = self.write_errors.pop(0)
            if error is not None:
                self.connected = False  # a failed write may also drop the link
                raise error

    async def disconnect(self) -> None:
        self.disconnect_calls += 1
        self.connected = False


class RecordingSleeper:
    def __init__(self) -> None:
        self.delays: list[float] = []

    async def __call__(self, delay: float) -> None:
        self.delays.append(delay)


@pytest.fixture
def sleeper() -> RecordingSleeper:
    return RecordingSleeper()


def make_sender(
    ble: FakeBleClient,
    sleeper: RecordingSleeper,
    callback=None,
) -> RobotCommandSender:
    return RobotCommandSender(
        ble_client=ble,  # type: ignore[arg-type]
        status_callback=callback,
        sleeper=sleeper,  # type: ignore[arg-type]
        retry_base_delay_s=0.1,
        retry_max_delay_s=0.5,
    )
