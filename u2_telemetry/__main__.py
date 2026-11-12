"""Entry point for the u2_telemetry service.

Run with: python -m u2_telemetry
"""

from __future__ import annotations

import asyncio
import logging

from .service import RobotTelemetryService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


async def main() -> None:
    service = RobotTelemetryService(ble_address="AA:BB:CC:DD:EE:FF")
    await service.run()


if __name__ == "__main__":
    asyncio.run(main())
