# Logical Components — u2-telemetry

Grounded in NFR requirements [all NFR requirements], functional-spec [functional-spec], contract-summary [contract-summary], and nfr-design questions [nfr-design-questions] (Q5: A — single logical component).

## Logical Components

### Component Inventory

| Component | Responsibility | Owns Data | Public API |
|-----------|---------------|-----------|------------|
| RobotTelemetry | Receives BLE telemetry, normalizes into RobotState, publishes RobotStateChanged | RobotState (ephemeral, in-memory) | `enqueue(RobotState)`, `run()` publisher loop |

### Component Boundaries (Q5: A)

U2 is a single logical component, `RobotTelemetry`, owning the full telemetry path: BLE receive → normalize → publish. This follows the principle that changes to internals do not ripple to other components — the BLE client, normalizer, and publisher are all internal to RobotTelemetry and expose only the publish side (Contract 2 topic) to consumers.

No split into separate BLE-receiver and event-publisher components (Q5: A), because:
- The two always deploy together (single U2 process on the Linux backend).
- The BLE receiver feeds the normalizer which feeds the publisher — a linear, non-branching path.
- Splitting would add indirection without reducing coupling (they share the same RobotState schema and event loop).

### Failure Domains & Blast Radius

| Failure | Blast Radius | Mitigation |
|---------|-------------|------------|
| BLE radio failure | U2 telemetry stops; U1 stops robot per BR1.4.3 | retry-with-backoff (NFR2.3), report to chat UI |
| Publish queue full | BLE reception blocks briefly | bounded queue, background publisher drains |
| U1 callback unavailable | Command status correlation degraded (best-effort) | telemetry continues (NFR2.4) |
| U3 StatsDisplay unavailable | Event dropped (fire-and-forget) | next event overwrites (Contract 2) |

### Component Isolation Strategy

- RobotTelemetry owns its data (RobotState) — no shared mutable state across boundaries.
- External interactions go through defined interfaces: BLE radio (inbound), Contract 2 topic (outbound), U1 sync callback for connection errors (inbound via Contract 1).
- Dependencies are acyclic: RobotTelemetry depends on bleak and the event bus; nothing depends on RobotTelemetry's internals.

### Shared Resource Identification

| Resource | Shared With | Sharing Model |
|----------|-------------|---------------|
| BLE radio (bleak client) | U1 (command sending) | multiplexed single connection |
| asyncio event loop | U2 internals only | single loop, one publisher coroutine |

### Bridge to Infrastructure Design

This logical component view informs Infrastructure Design: RobotTelemetry maps to one deployable unit on the Linux backend, bound to one BLE radio, with no infra dependencies beyond the OS Bluetooth stack (BlueZ) and the event bus used by Contract 2.

## Assumptions & Open Questions

None.
