"""BLE listener for Sphero Mini telemetry reception.

Uses bleak's BleakClient to connect to the Sphero Mini and subscribe to BLE
notification characteristics. Each notification is parsed into a raw telemetry
dict and handed to the ``on_telemetry`` callback. Connection errors and
disconnections are reported via the ``on_error`` callback.
"""

from __future__ import annotations

import asyncio
import json
from typing import Callable, Optional

from bleak import BleakClient

# Sphero Mini telemetry notification characteristic (illustrative UUID).
TELEMETRY_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"


class BLEListener:
    """Receives BLE telemetry notifications from a Sphero Mini.

    Args:
        address: BLE address of the Sphero Mini.
        on_telemetry: Callback invoked with each parsed telemetry dict.
        on_error: Callback invoked on connection errors/disconnections.
        client_class: bleak client class to instantiate (injectable for tests).
    """

    def __init__(
        self,
        address: str,
        on_telemetry: Callable[[dict], None],
        on_error: Callable[[Exception], None],
        client_class: type[BleakClient] = BleakClient,
    ) -> None:
        self.address = address
        self.on_telemetry = on_telemetry
        self.on_error = on_error
        self._client_class = client_class
        self._client: Optional[BleakClient] = None
        self._running = False

    async def connect(self) -> None:
        """Connect to the Sphero Mini BLE device."""
        self._client = self._client_class(self.address)
        await self._client.connect()

    async def disconnect(self) -> None:
        """Disconnect from the BLE device and stop the listen loop."""
        self._running = False
        if self._client and self._client.is_connected:
            await self._client.disconnect()

    async def start(self) -> None:
        """Run the connect → listen → reconnect loop until stopped.

        On connection error or disconnection, ``on_error`` (wired to
        ``connection_handler.handle_error`` by the service) is invoked and the
        loop retries with exponential backoff up to 3 attempts (NFR2.3). Once
        the retry budget is exhausted the loop stops instead of retrying in a
        tight unbounded loop; the retry-exhausted signal from
        ``connection_handler.handle_error`` is honored.
        """
        self._running = True
        attempt = 0
        while self._running:
            try:
                await self.connect()
                attempt = 0
                await self._listen()
            except Exception as exc:  # noqa: BLE001 - surface to error handler
                attempt += 1
                retry_remaining = await self._invoke_error(exc)
                if not self._running:
                    break
                if not retry_remaining or attempt >= 3:
                    # Retry budget exhausted (NFR2.3): stop the loop. The
                    # error has already been signaled to U1 via on_error.
                    self._running = False
                    break
                backoff = 2 ** (attempt - 1)
                await asyncio.sleep(backoff)

    async def _listen(self) -> None:
        """Subscribe to telemetry notifications and wait while connected."""

        def on_notification(sender: str, data: bytearray) -> None:
            try:
                raw = self._parse_telemetry(data)
            except Exception:
                return  # Malformed payload — skip silently.
            self.on_telemetry(raw)

        await self._client.start_notify(TELEMETRY_CHAR_UUID, on_notification)
        try:
            while self._running and self._client.is_connected:
                await asyncio.sleep(0.5)
        finally:
            await self._client.stop_notify(TELEMETRY_CHAR_UUID)

    async def _invoke_error(self, exc: Exception) -> bool:
        """Invoke the error handler, which may be sync or async.

        Returns whether another reconnect attempt should be made. When the
        error handler is ``connection_handler.handle_error`` this is its
        retry-exhausted signal (False once the budget is exhausted).
        """
        result = self.on_error(exc)
        if asyncio.iscoroutine(result):
            result = await result
        return bool(result) if isinstance(result, bool) else True

    @staticmethod
    def _parse_telemetry(data: bytearray) -> dict:
        """Parse raw BLE notification bytes into a telemetry dict.

        Expects a JSON payload such as {"direction": "forward", ...}.
        Lenient: missing fields are left absent so the normalizer applies
        placeholders.
        """
        text = bytes(data).decode("utf-8").strip()
        return json.loads(text)
