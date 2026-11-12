# Unit Test Instructions — u2-telemetry

Grounded in code-generation-plan [code-generation-plan], tech-stack-decisions [tech-stack-decisions], and NFR requirements [observability-requirements, reliability-requirements].

## Test Framework Setup

- **Framework:** pytest + coverage.py (Python backend, per NFR6 and tech-stack-decisions)
- **Methodology:** BDD (Given/When/Then scenarios first, then implement, then run tests — per team Testing Posture)
- **Configuration:** `pyproject.toml` with pytest configuration; `coverage.toml` or `[tool.coverage]` section in pyproject.toml for the 80% line-coverage floor
- **Dependencies:** `pytest`, `pytest-asyncio` (for async BLE/event-loop tests), `coverage.py`

## How to Run THIS UNIT's Tests

Run from the workspace root (the project's main folder), scoped to u2-telemetry only:

```bash
python -m pytest u2_telemetry/ -v --cov=u2_telemetry --cov-report=term-missing
```

This command is unit-scoped: it runs only u2-telemetry's test files. Do not use a bare project-wide command like `pytest` (Build and Test executes every unit's commands, so an unscoped command would rerun the whole suite once per unit).

The command must be runnable before the first test-first cycle (BDD Red step). Verify it before writing the first scenario.

## Expected Coverage Targets

- **80% line coverage** on u2-telemetry source (NFR7, mvp scope floor)
- Build and Test checks the coverage floor on the full assembled project suite, not per-unit
- A unit-scoped run can fail the coverage threshold on source that other units' tests cover while every selected test passes — this is not a failed test; record it with the unit's test results

## Mocking / Stubbing Guidance

- **BLE radio (bleak):** Mock the bleak `BleakClient` and notification callbacks in tests — do not require a physical Sphero Mini. Test lenient normalization (BR1.4.1: missing fields → dash/null placeholders) with synthetic telemetry payloads.
- **Event publishing (Contract 2):** Mock the event bus/WebSocket publish; verify fire-and-forget behavior (no retry on delivery failure).
- **U1 sync callback (Contract 1):** Mock the `CommandExecutionStatus` callback invocation; verify status is recorded and correlated with the corresponding RobotCommand.
- **Connection errors:** Simulate BLE disconnection and verify the error is signaled to U1 (chat UI + robot stop per BR1.4.3).

## Test Data Management

- **Synthetic telemetry payloads:** Complete RobotState (all five fields) and partial RobotState (missing fields filled with placeholders).
- **BLE connection states:** connected, disconnected, pairing, error.
- **Command execution statuses:** moving, stopped, error.
- No persistent test data — RobotState is append-only and ephemeral (in-memory).

## Test Scope (Standard Strategy)

Approximately 5-8 tests per component, covering:
- Happy path: telemetry receive → normalize → publish → U3 receives event
- Error/edge cases: at least two per module (e.g., BLE disconnect, partial telemetry, callback unavailable)
- Integration test stubs for key boundaries (U1 callback, Contract 2 event publish)

## Assumptions & Open Questions

None.
