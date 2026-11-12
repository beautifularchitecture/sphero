# Scalability Design — u2-telemetry

Grounded in NFR requirements [scalability-requirements], functional-spec [functional-spec], contract-summary [contract-summary], and nfr-design questions [nfr-design-questions] (Q6: A — single-consumer design).

## Scalability Design

### Consumer Model (Q6: A)

U2's RobotStateChanged event supports exactly one consumer: U3 StatsDisplay, per Contract 2 and NFR4.5. Event delivery is fire-and-forget with no retry; the next event overwrites any missed one. No fan-out, message bus, or multi-subscriber infrastructure is provisioned. This matches the single-robot MVP (NFR4.4: exactly one Sphero Mini).

### Scaling Approach

- **Horizontal scaling:** Not applicable to the MVP — U2 runs as a single instance on the Linux backend, bound to one BLE radio. No load balancer, no autoscaling group.
- **Data partitioning:** Not applicable — no persistent data store; telemetry is ephemeral (event-driven, fire-and-forget).
- **Queue-based decoupling:** An in-memory asyncio queue buffers events between BLE reception and publishing (bounded by the publish rate of 10 events/sec). No external message queue.

### Capacity Thresholds

| Parameter | Value | Basis |
|-----------|-------|-------|
| Concurrent robots | 1 | NFR4.4 (single-robot MVP) |
| Event subscribers | 1 (U3 StatsDisplay) | NFR4.5, Contract 2 |
| Sustained publish rate | 10 events/sec | NFR4.2 |
| Publish latency budget | 500ms | NFR4.1 |

## Assumptions & Open Questions

None.
