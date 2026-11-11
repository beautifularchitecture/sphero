# Security Requirements — u1-chat-command-core

Grounded in requirements analysis, functional design, and business rules.

## NFR2 — Bluetooth LE Security

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR2.1 | Bluetooth pairing | Sphero Mini paired once at setup; pairing required before any command execution | NFR2 |
| NFR2.2 | Bluetooth connection errors | Connection errors and disconnections reported to the chat UI; robot does not move on failed connection | NFR2 |

## Chat Input Validation (not mapped to inception NFR)

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR9.1 | Chat input validation | Chat messages validated: non-empty, not whitespace-only, valid UTF-8, matches known command pattern before translation | FR3 |
| NFR9.2 | Secret protection | OpenRouter API key stored in .env at project root, loaded at startup, never committed to version control | C-04 |
| NFR9.3 | Chat input authentication | Single-user model: chat messages come from the single authorized user (the operator); no per-message authentication required | FR3 |

## Assumptions & Open Questions

- Sphero Mini hardware is available and charged
- Linux machine with BlueZ and Bluetooth LE adapter is available
- OpenRouter API key is available and valid
