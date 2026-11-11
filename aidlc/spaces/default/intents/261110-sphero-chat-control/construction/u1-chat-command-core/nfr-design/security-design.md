# Security Design — u1-chat-command-core

Grounded in NFR requirements [security-requirements], functional design [functional-spec], and contract design [contract-summary].

## NFR2 — Bluetooth LE Security Design

| ID | Requirement | Design | Implementation |
|----|-------------|--------|----------------|
| NFR2.1 | Bluetooth pairing | Pair once at setup; stored pairing keys for reconnection. | BlueZ pairing agent with JustWorks or passkey entry; store bonding keys in system Bluetooth stack. |
| NFR2.2 | Bluetooth connection errors | Connection errors and disconnections reported to chat UI; robot stops on connection failure. | Bluetooth LE connection event handler; error events propagate to chat UI via WebSocket; robot motion stops on connection loss. |

## NFR9 — Chat Input Validation & Secret Protection

| ID | Requirement | Design | Implementation |
|----|-------------|--------|----------------|
| NFR9.1 | Chat input validation | Validate chat messages: non-empty, not whitespace-only, valid UTF-8, matches known command pattern before translation. | Input validation middleware in chat input endpoint; reject invalid messages with rephrase request in chat UI. |
| NFR9.2 | Secret protection | OpenRouter API key stored in .env at project root, loaded at startup, never committed to version control. | .env file in .gitignore; loaded via environment variable at backend startup; never logged or displayed in UI. |
| NFR9.3 | Chat input authentication | Single-user model: chat messages come from the single authorized user (the operator); no per-message authentication required. | No authentication layer; single-user desktop application; trust boundary is the local machine. |

## Security Architecture

- **Trust boundary**: Single-user desktop application; trust boundary is the local machine. No network authentication required for chat input.
- **Secret management**: OpenRouter API key in `.env` file, loaded via environment variable at backend startup, never committed to version control (`.gitignore`).
- **Bluetooth LE security**: Pairing once at setup; bonding keys stored in BlueZ; connection errors reported to chat UI.

## Assumptions & Open Questions

None.
