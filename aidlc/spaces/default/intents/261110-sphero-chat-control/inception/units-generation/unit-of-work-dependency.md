# Unit Dependency DAG — Sphero Mini Chat Control

Grounded in components [components], decisions [decisions], requirements [requirements], and user stories [stories].

## Dependency DAG

| Unit | Direct Depends On | Rationale |
|------|-------------------|-----------|
| U1 (u1-chat-command-core) | [] | Walking skeleton; no unit dependencies |
| U2 (u2-telemetry) | [U1] | Telemetry depends on command core for robot state context and execution status reporting |
| U3 (u3-stats-ui) | [U2] | Stats UI subscribes to telemetry events published by U2 |

The graph is cycle-free: U1 → U2 → U3 in dependency direction (U3 depends on U2 depends on U1). U1 can start immediately (walking skeleton); U2 starts once U1's command execution status interface is stable; U3 starts once U2's telemetry event format is stable.

## Integration Points

| From → To | Integration Point | Protocol | Data |
|-----------|-------------------|----------|------|
| U1 → U2 | Command execution status | Sync callback | commandId, status (moving/stopped/error), timestamp |
| U2 → U3 | RobotState telemetry events | Event (publish/subscribe) | direction, orientation, color, position, timestamp |

## Parallel Development Opportunities

| Units | Can Build in Parallel | Reason |
|-------|----------------------|--------|
| U1 alone (first) | Yes — walking skeleton | U1 has no unit dependencies; it is the first resolved DAG Unit |
| U2, U3 | No — sequential after U1 | U2 depends on U1; U3 depends on U2 |

No two non-skeleton Units can be built fully in parallel because the chain U1 → U2 → U3 is serial. However, U2's internal implementation (Bluetooth LE telemetry listener) can be developed alongside U1's command-sending code, with the integration point (command execution status callback) agreed first.

## Walking Skeleton

The walking skeleton is U1 (u1-chat-command-core): chat → robot → stats end-to-end, exercising chat input, AI translation, Bluetooth LE command sending, and robot movement. It is the first resolved DAG Unit and runs before U2 and U3.

**Running before later Units:** U1 demonstrates real robot motion from a chat message (forward/back/left/right/stop, speed control, LED color) with error handling. It does not yet show live stats (that's U2/U3), but it proves the command path end-to-end. U2 adds telemetry reception; U3 adds the stats UI rendering.

## Fenced YAML Edge Block

```yaml
units:
  - name: u1-chat-command-core
    kind: service
    depends_on: []
  - name: u2-telemetry
    kind: service
    depends_on: [u1-chat-command-core]
  - name: u3-stats-ui
    kind: ui
    depends_on: [u2-telemetry]
```

## Assumptions & Open Questions

None.
