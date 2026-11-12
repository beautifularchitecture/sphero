# Security Requirements — u2-telemetry

Grounded in functional-spec [functional-spec], rules [rules], requirements [requirements], contract-summary [contract-summary], and nfr-requirements questions [nfr-requirements-questions].

## Security Requirements

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR2.1 | Bluetooth LE encryption | Telemetry reception over BLE uses encryption (pairing required) | Q3 |
| NFR2.2 | No secrets in U2 | U2 uses no API keys, tokens, or secrets; no OpenRouter integration | Q7 |

## Security Rationale

- **NFR2.1 (BLE encryption):** Per Q3, U2's Bluetooth LE telemetry reception must use encryption with pairing required. This prevents eavesdropping on robot telemetry data on the local BLE link. The Sphero Mini (original) supports BLE pairing per NFR2.
- **NFR2.2 (No secrets in U2):** Per Q7, U2 does not use any API keys, tokens, or secrets. U2 does not integrate with OpenRouter (that is U1's responsibility per Contract 3). No `.env` or secret file is needed by U2.

## Assumptions & Open Questions

None.