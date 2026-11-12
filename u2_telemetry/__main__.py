"""Entry point for the u2_telemetry service.

Run with: python -m u2_telemetry

Configuration (environment variables, no hardcoded secrets or addresses):

    U2_BLE_ADDRESS   BLE address of the Sphero Mini (required; scan with
                     ``bluetoothctl``). No placeholder MAC is baked in.
"""

from __future__ import annotations

import asyncio
import logging
import os

from .event_bus import RobotStateEventBus
from .service import RobotTelemetryService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


async def _serve_websocket(bus: RobotStateEventBus) -> None:
    """Serve the FastAPI WebSocket endpoint if the transport stack is installed.

    The same ``bus`` instance the ``RobotTelemetryService`` publishes to is
    wired into the FastAPI app (via ``set_event_bus``) so WebSocket subscribers
    attach to the SAME ``RobotStateEventBus`` — otherwise RobotStateChanged
    events never reach a WebSocket client/U3 StatsDisplay (Contract 2).
    """
    try:
        import uvicorn  # type: ignore[import-not-found]
        from .api import app, set_event_bus  # type: ignore[import-not-found]
    except ImportError:
        logger.warning(
            "uvicorn/fastapi not installed; WebSocket endpoint unavailable. "
            "Install the transport stack to serve robot.state.changed over WebSocket."
        )
        return
    set_event_bus(bus)
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()


async def main() -> None:
    address = os.getenv("U2_BLE_ADDRESS")
    if not address:
        logger.error(
            "U2_BLE_ADDRESS environment variable is required (no hardcoded default). "
            "Scan for the Sphero Mini with bluetoothctl."
        )
        raise SystemExit(1)

    # SINGLE shared RobotStateEventBus instance. Its ``publish`` method is
    # injected into RobotTelemetryService and the instance itself is wired into
    # the FastAPI app (via set_event_bus in _serve_websocket), so the service
    # and the /ws/robot-state WebSocket endpoint share ONE bus — Contract 2
    # events flow end-to-end to WebSocket clients / U3 StatsDisplay.
    bus = RobotStateEventBus()
    service = RobotTelemetryService(
        ble_address=address,
        event_bus_publish=bus.publish,
    )

    await asyncio.gather(
        service.run(),
        _serve_websocket(bus),
    )


if __name__ == "__main__":
    asyncio.run(main())
