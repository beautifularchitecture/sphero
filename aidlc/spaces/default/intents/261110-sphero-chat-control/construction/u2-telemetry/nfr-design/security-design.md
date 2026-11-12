# Security Design — u2-telemetry

Grounded in NFR requirements [security-requirements], functional-spec [functional-spec], contract-summary [contract-summary], tech-stack-decisions [tech-stack-decisions], and nfr-design questions [nfr-design-questions] (Q1: A — retry-with-backoff only; Q3: B — accept any paired device).

## Security Design

### Authentication & Authorization

BLE pairing (encryption required, per NFR2.1) is the sole authentication mechanism for U2's telemetry reception. U2 accepts telemetry from any paired device (Q3: B) — encryption via pairing is sufficient for the single-robot MVP; no device-address allowlist is maintained. Authorization is implicit: the paired BLE peer is the robot; no per-user or per-role model exists in U2.

### Encryption Design

- **In transit:** BLE link-layer encryption with pairing required (NFR2.1, NFR2.1 → security-requirements NFR2.1). Protects telemetry eavesdropping on the local BLE link.
- **At rest:** U2 persists no telemetry, no RobotState history, and no secrets (NFR2.2). No `.env` or secret file is needed by U2 (NFR2.2 → security-requirements NFR2.2).
- **Secrets management:** U2 uses no API keys, tokens, or secrets. OpenRouter integration is U1's responsibility (Contract 3).

### Input Validation

Raw BLE telemetry is normalized into RobotState using lenient handling (BR1.4.1): missing fields are filled with dash/null placeholders rather than rejecting the event. This prevents malformed or partial telemetry from blocking the publish path (NFR4.6).

### Audit Logging

U2 logs BLE connection errors and disconnections only (NFR3.1). No per-event audit log is written for RobotStateChanged publishes (up to 10/sec, fire-and-forget per Contract 2). Correlation IDs are emitted per event for traceability (Q4: A) but are not persisted by U2.

## Assumptions & Open Questions

None.
