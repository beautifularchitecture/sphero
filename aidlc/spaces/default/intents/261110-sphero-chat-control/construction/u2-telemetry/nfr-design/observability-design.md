# Observability Design — u2-telemetry

Grounded in NFR requirements [observability-requirements], functional-spec [functional-spec], contract-summary [contract-summary], tech-stack-decisions [tech-stack-decisions], and nfr-design questions [nfr-design-questions] (Q4: A — correlation ID, no per-event logging).

## Observability Design

### Logging Strategy (Q4: A; NFR3.1)

U2 logs BLE connection errors and disconnections only — not every RobotStateChanged event (up to 10/sec, which would dominate log volume). Structured JSON logs include: event type, severity, timestamp, and (when available) the correlation ID. Log level is INFO for connection state changes, ERROR for BLE failures.

### Correlation ID & Tracing (Q4: A)

Each RobotStateChanged event carries a correlation ID generated at BLE receipt, propagated through normalization and publishing. The correlation ID is traceable via the Contract 2 topic (`robot.state.changed`) but is not persisted by U2. U3 StatsDisplay can surface it on the stats panel for end-to-end traceability of a single telemetry reading.

### Metrics Collection

| Metric | Type | Target | Source |
|--------|------|--------|--------|
| BLE connection state changes | counter | reported via U1 to chat UI | NFR3.2 |
| RobotStateChanged events published | counter | up to 10/sec sustained | NFR4.2 |
| Publish latency (p99) | histogram | < 500ms | NFR4.1 |
| BLE reconnection attempts | counter | ≤ 3 per drop | NFR2.3 |

### Alerting Rules

| Alert | Condition | Severity |
|-------|-----------|----------|
| BLE disconnected | connection state = disconnected > 30s | warning |
| Publish latency high | p99 latency > 500ms over 5 min | warning |
| Reconnect failure | 3 retries exhausted without restore | critical |

### Dashboard Specifications

The stats panel (U3) displays: current RobotState (direction, orientation, color, position, timestamp), connection status, and last-publish timestamp. No historical charting — telemetry is ephemeral.

### SLI/SLO Definitions

| SLI | Definition | SLO |
|-----|------------|-----|
| Telemetry publish availability | successful publishes / total publish attempts | ≥ 99% over a 30-day window |
| Publish latency | publishes below 500ms threshold / total publishes | ≥ 95% of publishes < 500ms |

### Correlation ID Propagation

The correlation ID is generated at BLE receipt, attached to the RobotState entity, and carried in the RobotStateChanged event payload's metadata. It enables U3 to correlate a displayed stat with the underlying BLE reading.

## Assumptions & Open Questions

None.
