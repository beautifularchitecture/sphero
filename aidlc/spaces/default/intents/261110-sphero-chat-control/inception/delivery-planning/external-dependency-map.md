# External Dependency Map — Sphero Mini Chat Control

Grounded in unit-of-work [unit-of-work], contract-summary [contract-summary], and requirements [requirements].

## External Dependencies

| Dependency | Owner | Lead Time | Blocks Bolt | Mitigation if Slips |
|------------|-------|-----------|-------------|---------------------|
| OpenRouter API key (.env) | User | User-provided; needed before Bolt 1 AI translation | Bolt 1 | Bolt 1 cannot demonstrate AI command translation without the key; chat input still works but commands are not generated |
| Sphero Mini Bluetooth LE pairing | User (Ubuntu desktop) | User performs pairing; needed before Bolt 1 walking skeleton | Bolt 1 | Bolt 1 cannot demonstrate robot motion without pairing; code can be written but not verified end-to-end |
| OpenRouter API (third-party API) | External service | Continuous availability during Bolt 1 development and testing | Bolt 1 | U1 error handling: API errors stop robot and show in chat UI; retry with exponential backoff (3 retries) |

## Dependency Notes

- OpenRouter API key is stored in `.env` at project root, never committed to version control (NFR C-04, affirmed at practices-discovery Q6)
- Sphero Mini Bluetooth LE pairing is a one-time setup; user confirmed they will perform it on their Ubuntu desktop
- Both dependencies are user-controlled, not team-controlled; no external team hand-offs required
- The MVP is fully AI-contained (aidlc-developer-agent solo mob); no external team dependencies

## Mapping to Bolts

| Bolt | External Dependencies |
|------|----------------------|
| Bolt 1 (U1) | OpenRouter API key, Sphero Mini Bluetooth LE pairing, OpenRouter API availability |
| Bolt 2 (U2) | Sphero Mini Bluetooth LE (telemetry reception) |
| Bolt 3 (U3) | None external (consumes U2's telemetry events internally) |

## Assumptions & Open Questions

- User will provide OpenRouter API key when ready (Delivery Planning Q5 answer)
- User will perform Sphero Mini Bluetooth LE pairing on Ubuntu desktop (Delivery Planning Q5 answer)
- Pairing instructions to be documented in README.md (user requested)
