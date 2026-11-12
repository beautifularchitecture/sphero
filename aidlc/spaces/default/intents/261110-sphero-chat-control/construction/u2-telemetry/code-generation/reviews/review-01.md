## Review

**Verdict:** NOT-READY
**Reviewer:** aidlc-architecture-reviewer-agent
**Date:** 2026-11-12T05:29:29Z
**Iteration:** 1
**Verdict Dictated:** no

### Findings

| ID | Severity | Location | Finding | Required action | Status |
|---|---|---|---|---|---|
| R-01 | Critical | u2_telemetry/__main__.py > line 20 (RobotTelemetryService construction without event_bus_publish); u2_telemetry/event_publisher.py > _default_publish method (lines 73-75); construction/u2-telemetry/infrastructure-design/infrastructure-specification.md > Infrastructure Services table (FastAPI + WebSocket row) | Contract 2 (U2 → U3 RobotStateChanged events on robot.state.changed) is not delivered in production. __main__.py constructs RobotTelemetryService without an event_bus_publish callable, so EventPublisher falls back to _default_publish, which is a no-op that only logs a debug message. Events are enqueued to an in-memory queue and never reach U3 StatsDisplay. The infrastructure design specifies FastAPI + WebSocket delivery on the robot.state.changed topic, but no FastAPI app, WebSocket endpoint, or event-bus integration exists anywhere in the 9 production files. traceability.json marks NFR4.1, NFR4.2, and NFR4.5 as OK targeting event_publisher.py, but that module delivers events nowhere. | Implement real Contract 2 event delivery (FastAPI WebSocket endpoint or event-bus publisher) on the robot.state.changed topic, wire it into RobotTelemetryService via event_bus_publish in __main__.py, and ensure production startup publishes RobotStateChanged events to U3. | New |
| R-02 | Major | u2_telemetry/ble_listener.py > start() method (lines 56-75); u2_telemetry/connection_handler.py > handle_error() method (lines 53-69); construction/u2-telemetry/nfr-design/reliability-design.md > Retry Policy table | BLE retry logic violates NFR2.3 (retry up to 3 times with exponential backoff, then stop). After the 3rd connect failure, start() stops sleeping but the while self._running loop continues, immediately re-attempting connect in a tight unbounded loop with no backoff and no stop condition. connection_handler.py handle_error() returns whether retries remain, but start() ignores this return value — two independent, uncoordinated retry counters. | Coordinate retry logic so BLEListener stops retrying after 3 attempts (honoring handle_error()'s false return) and does not enter a tight retry loop; align with NFR2.3's 3-retry, within-5-seconds contract. | New |
| R-03 | Major | u2_telemetry/models.py > RobotState dataclass; u2_telemetry/normalizer.py > normalize() method; u2_telemetry/event_publisher.py > run()/publish() path; construction/u2-telemetry/nfr-design/observability-design.md > Correlation ID & Tracing section | Correlation ID is not implemented despite the observability-design requiring it. The design states "Each RobotStateChanged event carries a correlation ID generated at BLE receipt, propagated through normalization and publishing," but RobotState has no correlation_id attribute, the normalizer generates none, and the publisher propagates none. End-to-end traceability of a telemetry reading (NFR3 observability) is degraded. | Add a correlation_id attribute to RobotState, generate it at BLE receipt in the normalizer/service, and propagate it through the RobotStateChanged event payload per the observability-design. | New |
| R-04 | Minor | aidlc/spaces/default/intents/261110-sphero-chat-control/construction/u2-telemetry/code-generation/code-summary.md > Files Created table (test_normalizer.py row) and Test Coverage Summary | The code-summary test-count table under-counts test_normalizer.py (lists 8 scenarios; the file has 9 test functions). The table's implied total (38) conflicts with the claimed "39 tests passed" (verified correct by test run), though the headline figure is accurate. | Correct the per-file scenario counts in code-summary.md so the table matches the actual test files (test_normalizer.py = 9). | New |
| R-05 | Minor | u2_telemetry/__main__.py > line 20 | The production entry point hardcodes ble_address="AA:BB:CC:DD:EE:FF", a placeholder MAC address that will not connect to any real Sphero Mini. The DEPLOYMENT doc acknowledges the address must be set, but the shipped entry point is non-functional for production without editing. | Make the BLE address configurable (environment variable or config file) with a documented default, rather than a hardcoded placeholder in __main__.py. | New |

### Validation Tool Results

| Tool | Result | Interpretation |
|---|---|---|
| python3 -m pytest u2_telemetry/ -v --cov=u2_telemetry --cov-report=term-missing | PASS: 39 passed, 94.59% coverage (fail_under=80 met) | Confirms code-summary claims of 39 tests and 94.59% coverage are accurate; coverage floor satisfied for this unit's scoped run |
| Manual import-graph review of all 9 source files | PASS: no circular dependencies | models→(none internal), normalizer→models, event_publisher→models, service→ble_listener/callback_handler/connection_handler/event_publisher/models/normalizer, __main__→service, __init__→models/normalizer/service; no cycles |

### Summary

NOT-READY: Contract 2 event delivery is a production no-op (events never reach U3), the BLE retry loop violates NFR2.3 by retrying unboundedly after 3 attempts, and correlation IDs required by the observability design are absent. All 39 tests pass at 94.59% coverage and there are no circular dependencies, but the core integration contract cannot be fulfilled as shipped.
