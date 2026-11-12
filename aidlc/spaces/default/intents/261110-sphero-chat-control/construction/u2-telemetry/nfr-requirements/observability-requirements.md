# Observability Requirements — u2-telemetry

Grounded in functional-spec [functional-spec], rules [rules], requirements [requirements], contract-summary [contract-summary], and nfr-requirements questions [nfr-requirements-questions].

## Observability Requirements

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR3.1 | Telemetry event logging | U2 logs BLE connection errors and disconnections; does not log every RobotStateChanged event (deduplication not applied) | Q4 |
| NFR3.2 | Connection status reporting | U2 reports BLE connection state (connected, disconnected, pairing, error) through U1 to the chat UI | Q4, Q2 |
| NFR3.3 | RobotState observability | RobotState entity (direction, orientation, color, position, timestamp) is observable via the RobotStateChanged event per Contract 2 | NFR3, BR1.4.2 |

## Observability Rationale

- **NFR3.1 (Telemetry event logging):** Per Q4, U2 logs only errors and connection state changes, not every telemetry event. This avoids log noise from high-frequency telemetry (up to 10 events/sec per NFR4.2) while preserving error visibility.
- **NFR3.2 (Connection status):** Per Q4 and Q2, U2 reports BLE connection state changes through U1 to the chat UI. Connection status (connected, disconnected, pairing, error) is observable in the UI per US1.4 AC1.4.2.
- **NFR3.3 (RobotState observability):** Per NFR3 and BR1.4.2, every RobotState (direction, orientation, color, position, timestamp) is observable via the RobotStateChanged event consumed by U3 StatsDisplay. This satisfies the stats panel observability requirement per NFR3.

## Assumptions & Open Questions

None.