# Reliability Design — u2-telemetry

Grounded in NFR requirements [reliability-requirements], functional-spec [functional-spec], contract-summary [contract-summary], and nfr-design questions [nfr-design-questions] (Q1: A — retry-with-backoff only).

## Reliability Design

### Resilience Patterns (Q1: A)

No circuit breaker is introduced (Q1: A). U2 relies on retry-with-backoff alone, matching NFR2.3 exactly: auto-reconnect within 5 seconds of a BLE telemetry connection drop, retrying up to 3 times with exponential backoff. This keeps the design simple and avoids adding a circuit breaker whose failure modes would need their own tuning for a single-robot MVP.

### Retry Policy

| Parameter | Value | Basis |
|-----------|-------|-------|
| Reconnect window | within 5s of BLE drop | NFR2.3 |
| Max retries | 3 | NFR2.3 |
| Backoff | exponential | NFR2.3 |
| Retryable errors | BLE connection drop, GATT errors | transient only |
| Non-retryable | pairing failure, unsupported robot | fail fast |

### Health Checks

A shallow connection-state check reports BLE connection state (connected, disconnected, pairing, error) through U1 to the chat UI (NFR3.2 → U1 owns the chat UI). No deep dependency health check is needed — U2's only external dependency is the BLE radio itself.

### Graceful Degradation (NFR2.4)

When U1's CommandExecutionStatus callback is unavailable, U2 continues publishing telemetry events. Command status correlation is best-effort and does not block telemetry flow (per Contract 1 error handling: U1 logs and continues).

### Failover & Backup

No replication or failover — single instance, single BLE radio, no persistent state. Telemetry is ephemeral (fire-and-forget); a dropped event is overwritten by the next one (Contract 2).

## Assumptions & Open Questions

None.
