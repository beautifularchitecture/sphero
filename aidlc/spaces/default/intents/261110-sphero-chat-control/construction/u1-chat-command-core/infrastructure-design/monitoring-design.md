# Monitoring Design — u1-chat-command-core

Grounded in NFR requirements [observability-requirements], functional design [functional-spec], and contract design [contract-summary].

## Metrics & KPIs

| Metric | Source | Threshold | Why it matters |
|--------|--------|-----------|----------------|
| Backend process health | `/health` HTTP GET endpoint | Returns 200 when healthy | Detects backend process crashes or hangs |
| Bluetooth LE connection status | Bluetooth LE adapter state | Connected vs disconnected | Robot commands cannot be sent when disconnected |
| Chat message processing time | Backend application logs | Warning if > 2 seconds | Detects agent/model latency issues |
| Bluetooth command round-trip | Bluetooth LE adapter | Warning if > 500ms | Detects Bluetooth connection degradation |
| OpenRouter API response time | Backend application logs | Warning if > 3 seconds | Detects model inference delays |
| Robot command success rate | RobotCommand error/success counts | Warning if error rate > 5% | Detects command execution failures |
| System memory/CPU usage | Host OS metrics | Warning if > 80% | Detects resource exhaustion on single-user machine |

## Alerts

| Alert | Condition | Severity | Routes to |
|-------|-----------|----------|-----------|
| Backend health check failed | `/health` returns non-200 for 2 consecutive checks | Error | Chat UI error banner |
| Bluetooth LE disconnected | Bluetooth LE connection lost | Error | Chat UI error banner; robot stops motion |
| Chat message processing slow | Processing time > 2 seconds | Warning | Chat UI warning message |
| Bluetooth command timeout | No ACK within 500ms | Warning | Retry once with backoff; error to chat UI if retry fails |
| High CPU/memory usage | Host CPU/memory > 80% for 5 minutes | Warning | Chat UI warning message |
| OpenRouter API error | OpenRouter API returns error or timeout | Error | Chat UI error message; stop robot motion |

## SLIs / SLOs

| SLI | SLO target | Measurement window |
|-----|------------|--------------------|
| Backend availability | 99.5% of health checks return 200 | 5-minute rolling window |
| Bluetooth LE connection uptime | 95% of time connected when robot is awake | Per robot session |
| Chat message processing p95 latency | ≤ 5 seconds end-to-end | Per message |
| Bluetooth command success rate | ≥ 95% of commands acknowledged | Per robot session |

## Logs & Tracing

| Log Type | Source | Retention | Destination |
|----------|--------|-----------|-------------|
| Chat input received | ChatInput component | 7 days | Local file log (structured JSON) |
| Agent command emitted | AgentCommand component | 7 days | Local file log (structured JSON) |
| Bluetooth command sent | RobotCommand component | 7 days | Local file log (structured JSON) |
| Robot state telemetry | RobotTelemetry component | 7 days | Local file log (structured JSON) |
| Errors | All components | 30 days | Local file log (structured JSON); shown in chat UI |
| Access/error logs | FastAPI backend | 7 days | Standard uvicorn access/error logs |

## Assumptions & Open Questions

- Backend health endpoint (`/health`) is basic liveness check only; no deep dependency checks (does not verify Bluetooth LE or OpenRouter connectivity)
- Chat UI is the primary alerting channel; no email/SMS alerts for a single-user desktop application
- Logs are stored locally on the Linux host; no centralized log aggregation for a single-user project