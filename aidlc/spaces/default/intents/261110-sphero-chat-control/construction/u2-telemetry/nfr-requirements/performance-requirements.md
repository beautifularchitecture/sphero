# Performance Requirements — u2-telemetry

Grounded in functional-spec [functional-spec], rules [rules], requirements [requirements], contract-summary [contract-summary], and nfr-requirements questions [nfr-requirements-questions].

## Performance Requirements

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR4.1 | Telemetry event publish latency | Raw BLE telemetry to RobotStateChanged event published within 500ms | Q1 |
| NFR4.2 | Telemetry event publishing throughput | Up to 10 RobotStateChanged events per second sustained | Q6 |
| NFR4.3 | RobotState normalization latency | Raw telemetry normalized into RobotState within 100ms of receipt | Q1 (derived) |

## Performance Rationale

- **NFR4.1 (500ms publish latency):** Per Q1, U2 must publish RobotStateChanged events within 500ms of receiving raw BLE telemetry. This ensures the stats panel in U3 reflects near-real-time robot state per NFR3 (refreshed on every robot state change).
- **NFR4.2 (10 events/sec):** Per Q6, U2 must sustain up to 10 RobotStateChanged events per second. This accommodates the Sphero Mini's telemetry update rate without event loss.
- **NFR4.3 (100ms normalization):** Derived from Q1; leaves 400ms of the 500ms budget for event publishing after normalization.

## Assumptions & Open Questions

None.