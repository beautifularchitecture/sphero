"""BDD scenarios for the u2_telemetry entry point (__main__).

Given/When/Then scenarios:
- Happy path: with U2_BLE_ADDRESS set, main() creates a single shared
  RobotStateEventBus and wires its publish into RobotTelemetryService and the
  same instance into the FastAPI app (single shared bus — Contract 2).
- Error/edge: without U2_BLE_ADDRESS, main() raises SystemExit(1) (no
  hardcoded default address).
"""

from __future__ import annotations

import asyncio

import pytest

from u2_telemetry.event_bus import RobotStateEventBus


@pytest.mark.asyncio
async def test_main_requires_ble_address(monkeypatch):
    """Given U2_BLE_ADDRESS is not set
    When main() is invoked
    Then it raises SystemExit(1) rather than using a hardcoded default."""
    monkeypatch.delenv("U2_BLE_ADDRESS", raising=False)

    from u2_telemetry import __main__ as main_module

    with pytest.raises(SystemExit) as exc_info:
        await main_module.main()

    assert exc_info.value.code == 1


@pytest.mark.asyncio
async def test_main_creates_shared_bus_and_wires_service(monkeypatch):
    """Given U2_BLE_ADDRESS is set
    When main() runs
    Then a single RobotStateEventBus is created, its publish is injected into
    RobotTelemetryService, and the same bus instance is wired into the API app
    (single shared bus — Contract 2)."""
    monkeypatch.setenv("U2_BLE_ADDRESS", "AA:BB:CC:DD:EE:FF")

    import u2_telemetry.api as api_module
    from u2_telemetry import __main__ as main_module

    api_module._bus = None  # clean DI state

    captured: dict = {}

    async def fake_run(self) -> None:
        captured["service"] = self
        return

    async def fake_serve_websocket(bus: RobotStateEventBus) -> None:
        # Mirror the real _serve_websocket wiring: the same bus instance is
        # set on the FastAPI app so WebSocket subscribers share the service's bus.
        api_module.set_event_bus(bus)
        return

    # Patch out blocking BLE/uvicorn work so main() completes deterministically.
    monkeypatch.setattr(main_module.RobotTelemetryService, "run", fake_run)
    monkeypatch.setattr(main_module, "_serve_websocket", fake_serve_websocket)

    await main_module.main()

    service = captured["service"]
    # The single bus's publish method is wired into the service publisher.
    assert service.publisher._publish is not None
    bus = service.publisher._publish.__self__
    assert isinstance(bus, RobotStateEventBus)
    # The same bus instance is set on the FastAPI app (shared transport).
    assert api_module._get_bus() is bus

    api_module._bus = None
