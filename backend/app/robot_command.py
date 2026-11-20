"""Bluetooth LE command sender for the Sphero Mini.

The BLE stack is injected via :class:`BleClient`; the production adapter imports
``bleak`` lazily. No robot or BlueZ installation is needed to run the test suite.
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timezone
from typing import Any, Protocol

from .config import (
    DEFAULT_BLE_COMMAND_CHARACTERISTIC_UUID,
    DEFAULT_BLE_SERVICE_UUID,
    DEFAULT_RETRY_BASE_DELAY_S,
    DEFAULT_RETRY_MAX_DELAY_S,
    configure_logging,
    log_event,
)
from .models import (
    MOVEMENT_COMMANDS,
    CommandExecutionStatus,
    CommandSource,
    CommandStatus,
    CommandType,
    RobotCommand,
)

MAX_SEND_ATTEMPTS = 2  # initial write + one retry (NFR4.4)


class BleConnectionError(RuntimeError):
    """The BLE link could not be established or maintained."""


class RobotCommandError(RuntimeError):
    """The robot could not execute a command; safe to show in the chat UI."""

    def __init__(self, message: str, code: str = "bluetooth") -> None:
        super().__init__(message)
        self.code = code

    def to_chat_error(self) -> dict[str, str]:
        return {
            "type": self.code,
            "message": str(self),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class BleClient(Protocol):
    """Injected BLE boundary (write uses response=True to get an ACK)."""

    async def connect(self) -> None: ...

    async def is_connected(self) -> bool: ...

    async def write_gatt(self, service_uuid: str, characteristic_uuid: str, payload: bytes) -> None: ...

    async def disconnect(self) -> None: ...


class BleakBleClient:
    """Production BLE adapter. ``bleak`` is imported only when first used."""

    def __init__(
        self,
        address: str,
        service_uuid: str = DEFAULT_BLE_SERVICE_UUID,
        characteristic_uuid: str = DEFAULT_BLE_COMMAND_CHARACTERISTIC_UUID,
    ) -> None:
        self._address = address
        self._service_uuid = service_uuid
        self._characteristic_uuid = characteristic_uuid
        self._client: Any = None

    async def connect(self) -> None:
        try:
            from bleak import BleakClient
        except ImportError as exc:
            raise BleConnectionError(
                "bleak is required to control the robot. Install the runtime dependencies."
            ) from exc
        try:
            self._client = BleakClient(self._address)
            await self._client.connect()
        except Exception as exc:
            self._client = None
            raise BleConnectionError(
                f"Could not connect to robot at {self._address}: {exc}"
            ) from exc

    async def is_connected(self) -> bool:
        return bool(self._client is not None and getattr(self._client, "is_connected", False))

    async def write_gatt(self, service_uuid: str, characteristic_uuid: str, payload: bytes) -> None:
        if not await self.is_connected():
            raise BleConnectionError("BLE client is not connected to the robot")
        try:
            await self._client.write_gatt_char(characteristic_uuid, payload, response=True)
        except Exception as exc:
            raise BleConnectionError(f"BLE write failed: {exc}") from exc

    async def disconnect(self) -> None:
        if self._client is not None:
            await self._client.disconnect()
            self._client = None


def encode_command(command: RobotCommand) -> bytes:
    """Encode a command as compact UTF-8 JSON for the robot's control characteristic."""
    payload: dict[str, Any] = {
        "commandId": command.command_id,
        "command": command.command.value,
    }
    if command.speed is not None:
        payload["speed"] = command.speed.value
    if command.color is not None:
        payload["color"] = command.color.value
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


class RobotCommandSender:
    """Send commands with one retry, reconnect-on-failure, and U2 status reporting."""

    def __init__(
        self,
        ble_client: BleClient,
        status_callback=None,
        sleeper=None,
        retry_base_delay_s: float = DEFAULT_RETRY_BASE_DELAY_S,
        retry_max_delay_s: float = DEFAULT_RETRY_MAX_DELAY_S,
        logger=None,
    ) -> None:
        self._ble = ble_client
        self._status_callback = status_callback
        self._sleeper = sleeper or asyncio.sleep
        self._retry_base_delay_s = retry_base_delay_s
        self._retry_max_delay_s = retry_max_delay_s
        self._logger = logger or configure_logging()

    async def _reconnect(self) -> None:
        """Drop a stale link; the next attempt establishes a fresh connection."""
        try:
            await self._ble.disconnect()
        except Exception as exc:  # best-effort; the next attempt will surface a real failure
            log_event(self._logger, "ble_disconnect_failed", error_type=type(exc).__name__)

    async def _report_status(self, command: RobotCommand, status: CommandStatus) -> None:
        """Report Contract 1 status to U2; retry once, then log and continue (BR1.4)."""
        if self._status_callback is None:
            return
        payload = CommandExecutionStatus(command_id=command.command_id, status=status)
        for attempt in range(1, MAX_SEND_ATTEMPTS + 1):
            try:
                self._status_callback(payload)
                return
            except Exception as exc:
                log_event(
                    self._logger,
                    "status_report_failed",
                    command_id=command.command_id,
                    attempt=attempt,
                    error_type=type(exc).__name__,
                )
                if attempt < MAX_SEND_ATTEMPTS:
                    await self._sleeper(self._retry_base_delay_s)
        log_event(self._logger, "status_report_abandoned", command_id=command.command_id)

    async def send(self, command: RobotCommand) -> CommandExecutionStatus:
        """Execute one robot command; raise :class:`RobotCommandError` on failure."""
        started = time.monotonic()
        payload = encode_command(command)
        last_error: Exception | None = None

        for attempt in range(1, MAX_SEND_ATTEMPTS + 1):
            try:
                if not await self._ble.is_connected():
                    await self._ble.connect()
                await self._ble.write_gatt(
                    DEFAULT_BLE_SERVICE_UUID, DEFAULT_BLE_COMMAND_CHARACTERISTIC_UUID, payload
                )
                status = (
                    CommandStatus.MOVING
                    if command.command in MOVEMENT_COMMANDS
                    else CommandStatus.STOPPED
                )
                command.status = status
                await self._report_status(command, status)
                log_event(
                    self._logger,
                    "command_executed",
                    command_id=command.command_id,
                    command=command.command.value,
                    status=status.value,
                    attempt=attempt,
                    duration_ms=round((time.monotonic() - started) * 1000, 2),
                )
                return CommandExecutionStatus(
                    command_id=command.command_id, status=status
                )
            except Exception as exc:  # BLE SDKs raise varied errors at this boundary
                last_error = exc
                log_event(
                    self._logger,
                    "robot_command_failed",
                    command_id=command.command_id,
                    attempt=attempt,
                    error_type=type(exc).__name__,
                )
                if attempt < MAX_SEND_ATTEMPTS:
                    await self._reconnect()
                    delay = min(
                        self._retry_base_delay_s * (2 ** (attempt - 1)),
                        self._retry_max_delay_s,
                    )
                    await self._sleeper(delay)

        command.status = CommandStatus.ERROR
        await self._report_status(command, CommandStatus.ERROR)
        raise RobotCommandError(
            "The robot is unreachable right now. Check Bluetooth and try again."
        ) from last_error

    async def stop(self) -> None:
        """Best-effort stop used by the chat error path (BR1.3)."""
        await self.send(RobotCommand(command=CommandType.STOP, source=CommandSource.API))
