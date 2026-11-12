# Reliability Requirements — u2-telemetry

Grounded in functional-spec [functional-spec], rules [rules], requirements [requirements], contract-summary [contract-summary], and nfr-requirements questions [nfr-requirements-questions].

## Reliability Requirements

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR2.3 | BLE telemetry reconnection | U2 reconnects automatically within 5 seconds of BLE telemetry connection drop, retrying up to 3 times with exponential backoff | Q2 |
| NFR2.4 | Graceful degradation when U1 unavailable | U2 continues publishing telemetry events; CommandExecutionStatus correlation is best-effort (per Contract 1 error handling) | Q5 |
| NFR4.6 | Partial telemetry tolerance | U2 publishes RobotState with dash/null placeholders for missing fields; does not block on incomplete telemetry (lenient normalization per BR1.4.1) | Q1 (derived), BR1.4.1 |

## Reliability Rationale

- **NFR2.3 (BLE reconnection):** Per Q2, U2 must auto-reconnect within 5 seconds of a BLE telemetry connection drop, with up to 3 retries using exponential backoff. This ensures the stats panel recovers quickly from transient BLE issues per US1.5 AC1.5.4 (robot disconnect handling).
- **NFR2.4 (Graceful degradation):** Per Q5 and Contract 1 error handling, when U1's CommandExecutionStatus callback is unavailable, U2 continues publishing telemetry events. Command status correlation is best-effort and does not block telemetry flow.
- **NFR4.6 (Partial telemetry tolerance):** Per BR1.4.1 (lenient normalization), U2 publishes RobotState events even with missing fields (filled with dash/null placeholders). This prevents incomplete telemetry from blocking the stats panel update flow per NFR3.

## Assumptions & Open Questions

None.