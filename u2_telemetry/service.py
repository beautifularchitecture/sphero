"""RobotTelemetry service — single component owning receive → normalize → publish.

U2's single logical component (logical-components Q5: A) that receives BLE
telemetry from the Sphero Mini, normalizes it into a RobotState, and publishes
RobotStateChanged events on ``robot.state.changed`` per Contract 2.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Awaitable, Callable, Optional

from bleak import BleakClient

from .ble_listener import BLEListener
from .callback_handler import CommandStatusCallbackHandler
from .connection_handler import ConnectionHandler
from .event_publisher import EventPublisher
from .models import RobotState
from .normalizer import RobotStateNormalizer

logger = logging.getLogger(__name__)


class RobotTelemetryService:
    """U2 RobotTelemetry service.

    Wires the BLE listener, normalizer, event publisher, status callback
    handler, and connection handler into a single telemetry path:

        BLE receive → normalize → enqueue → publish (fire-and-forget)

    Args:
        ble_address: BLE address of the Sphero Mini.
        event_bus_publish: Optional async publish callable for Contract 2
            event delivery. Injected for testing.
        u1_status_callback: Optional downstream callable for CommandExecutionStatus
            correlation from U1.
        u1_error_signal: Optional callable invoked on BLE errors (U1 chat UI).
        client_class: bleak client class to instantiate (injectable for tests).
    """

    def __init__(
        self,
        ble_address: str,
        event_bus_publish: Optional[
            Callable[[str, RobotState], Awaitable[None]]
        ] = None,
        u1_status_callback: Optional[Callable[[str, str, str], None]] = None,
        u1_error_signal: Optional[Callable[[Exception], None]] = None,
        client_class: type[BleakClient] = BleakClient,
    ) -> None:
        self.ble_address = ble_address
        self.publisher = EventPublisher(publish=event_bus_publish)
        self.normalizer = RobotStateNormalizer()
        self.status_handler = CommandStatusCallbackHandler(
            on_status=u1_status_callback
        )
        self.connection = ConnectionHandler(
            on_error_signal=u1_error_signal or self._default_error_signal,
        )
        self._listener: Optional[BLEListener] = None
        self._client_class = client_class

    def _default_error_signal(self, exc: Exception) -> None:
        logger.error("BLE error (no U1 error signal wired): %s", exc)

    def _on_telemetry(self, raw_telemetry: dict) -> None:
        """Handle a raw BLE telemetry event: normalize and enqueue for publish.

        Called synchronously from the BLE notification callback; schedules the
        async enqueue on the running event loop.
        """
        try:
            state = self.normalizer.normalize(raw_telemetry)
        except Exception as exc:  # noqa: BLE001 - normalization must not block
            logger.error("Normalization failed: %s", exc)
            return
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.publisher.enqueue(state))
        except RuntimeError:
            logger.error("No event loop running; telemetry event dropped")

    def handle_command_status(self, command_id: str, status: str, timestamp: str) -> None:
        """U1 invokes this sync callback with CommandExecutionStatus (Contract 1)."""
        self.status_handler.handle_status(command_id, status, timestamp)

    async def run(self) -> None:
        """Run the service: start the publisher and BLE listener loop."""
        await self.publisher.start()
        self._listener = BLEListener(
            self.ble_address,
            on_telemetry=self._on_telemetry,
            on_error=self.connection.handle_error,
            client_class=self._client_class,
        )
        await self._listener.start()

    async def stop(self) -> None:
        """Stop the publisher and disconnect the BLE listener."""
        await self.publisher.stop()
        if self._listener:
            await self._listener.disconnect()
