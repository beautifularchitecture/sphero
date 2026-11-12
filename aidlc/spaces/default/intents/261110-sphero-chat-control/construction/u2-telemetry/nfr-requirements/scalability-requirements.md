# Scalability Requirements — u2-telemetry

Grounded in functional-spec [functional-spec], rules [rules], requirements [requirements], contract-summary [contract-summary], and nfr-requirements questions [nfr-requirements-questions].

## Scalability Requirements

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR4.4 | Single-robot telemetry scale | U2 supports telemetry from exactly one Sphero Mini robot (single-robot MVP per C-02) | Q6 |
| NFR4.5 | Event subscriber scale | U2's RobotStateChanged event supports one consumer (U3 StatsDisplay) per Contract 2 | Q6 |

## Scalability Rationale

- **NFR4.4 (Single-robot):** Per C-02 (no multi-robot support in MVP), U2 handles telemetry from one Sphero Mini only. No robot discovery, pairing management, or multi-robot routing is required.
- **NFR4.5 (Single consumer):** Per Contract 2, U2 publishes RobotStateChanged events to one consumer (U3 StatsDisplay). No fan-out, message bus, or multi-subscriber infrastructure is required.

## Assumptions & Open Questions

None.