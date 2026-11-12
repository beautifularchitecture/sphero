# Monitoring Design — u2-telemetry

Grounded in observability-design [observability-design], NFR requirements [observability-requirements], and infrastructure-specification [infrastructure-specification].

## Metrics & KPIs

| Metric | Source | Threshold | Why it matters |
|--------|--------|-----------|----------------|
| BLE connection state | systemd + U2 log | disconnected > 30s | Telemetry stops; robot must be stopped per BR1.4.3 |
| RobotStateChanged events published | U2 app metric | > 10/sec sustained | Exceeds NFR4.2 capacity; may indicate telemetry storm |
| Publish latency (p99) | U2 app metric | > 500ms | Violates NFR4.1 latency budget |
| BLE reconnection attempts | U2 app metric | > 3 per drop | NFR2.3 retry budget exhausted |
| U2 process uptime | systemd | < 99.9% over 30 days | Service availability SLO |

## Alerts

| Alert | Condition | Severity | Routes to |
|-------|-----------|----------|-----------|
| BLE disconnected | connection state = disconnected for > 30s | warning | U1 chat UI (robot stopped) |
| Publish latency high | p99 latency > 500ms over 5 min | warning | U1 chat UI / ops |
| Reconnect failure | 3 retries exhausted without BLE restore | critical | U1 chat UI / ops |
| U2 process down | systemd service not active | critical | ops (on-call) |

## SLIs / SLOs

| SLI | SLO target | Measurement window |
|-----|------------|---------------------|
| Telemetry publish availability | successful publishes / total publish attempts ≥ 99% | 30 days |
| Publish latency | publishes below 500ms / total publishes ≥ 95% | 30 days |
| BLE connection availability | connected time / total time ≥ 99% | 30 days |

## Logs & Tracing

- **Log aggregation:** U2 writes structured JSON logs to stdout; systemd captures them to the journal. CloudWatch Logs agent forwards the journal to CloudWatch (30-day retention). Logs include BLE connection errors and disconnections only (NFR3.1 — not every RobotStateChanged event).
- **Tracing:** Each RobotStateChanged event carries a correlation ID (Q4=A) generated at BLE receipt and propagated through normalization and publishing. The ID is traceable via the Contract 2 topic but not persisted by U2. U3 StatsDisplay can surface it on the stats panel.
- **Dashboard specifications:** The stats panel (U3) displays current RobotState (direction, orientation, color, position, timestamp), connection status (connected/disconnected/pairing/error), and last-publish timestamp. No historical charting — telemetry is ephemeral.

## Assumptions & Open Questions

None.
