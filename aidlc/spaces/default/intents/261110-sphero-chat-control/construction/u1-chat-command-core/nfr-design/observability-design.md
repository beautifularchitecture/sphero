# Observability Design — u1-chat-command-core

Grounded in NFR requirements [observability-requirements], functional design [functional-spec], and contract design [contract-summary].

## NFR3 — Stats Observability Design

| ID | Requirement | Design | Implementation |
|----|-------------|--------|----------------|
| NFR3.1 | Stats panel data | Direction, orientation, color, and position refreshed on every robot state change. | Bluetooth LE telemetry listener; normalized RobotState; published via WebSocket to frontend. |
| NFR3.2 | Connection status | Connection status indicator (connected/disconnected/pairing/error) shown in UI. | Bluetooth LE connection state machine; status updates via WebSocket to frontend. |
| NFR3.3 | Error visibility | Errors shown in chat UI with plain-language message. | Error events from Bluetooth LE and backend; rendered as chat messages. |
| NFR3.4 | Logging standards | Application logs structured events (chat received, command emitted, command executed, error) with timestamps. | Structured JSON logging; ISO-8601 timestamps; all integration boundary events logged. |
| NFR3.5 | Alerting thresholds | Connection errors and Bluetooth failures alert in chat UI within 5 seconds. | Immediate error propagation to chat UI; no batching or delay. |
| NFR3.6 | Backend health/alerting | Backend exposes health check endpoint at /health (HTTP GET, returns 200 when healthy; basic liveness check only); backend errors logged and surfaced in chat UI. | HTTP GET /health endpoint; returns 200 when backend process is healthy; no deep dependency checks. |

## Observability Architecture

- **Telemetry ingestion**: Bluetooth LE telemetry listener receives direction, orientation, color, position from Sphero Mini; normalizes into RobotState; publishes via WebSocket to frontend.
- **Error surfacing**: All errors (Bluetooth, backend, OpenRouter) surfaced in chat UI with plain-language messages within 5 seconds.
- **Health endpoint**: `/health` (HTTP GET) returns 200 when backend process is healthy; basic liveness check only, no deep dependency checks.

## Assumptions & Open Questions

None.
