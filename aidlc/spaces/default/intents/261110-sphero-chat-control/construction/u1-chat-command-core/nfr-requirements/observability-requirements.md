# Observability Requirements — u1-chat-command-core

Grounded in requirements analysis, functional design, and business rules.

## NFR3 — Stats Observability

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR3.1 | Stats panel data | Direction, orientation, color, and position refreshed on every robot state change | NFR3 |
| NFR3.2 | Connection status | Connection status indicator (connected/disconnected/pairing/error) shown in UI | NFR3 |
| NFR3.3 | Error visibility | Errors shown in chat UI with plain-language message | NFR3 |
| NFR3.4 | Logging standards | Application logs structured events (chat received, command emitted, command executed, error) with timestamps | NFR3 |
| NFR3.5 | Alerting thresholds | Connection errors and Bluetooth failures alert in chat UI within 5 seconds | NFR3 |
| NFR3.6 | Backend health/alerting | Backend exposes health check endpoint at /health (HTTP GET, returns 200 when healthy; basic liveness check only — no deep dependency checks); backend errors logged and surfaced in chat UI | NFR3 |

## Assumptions & Open Questions

- Sphero Mini hardware is available and charged
- Chat UI is the primary alerting channel for backend health and connection errors
