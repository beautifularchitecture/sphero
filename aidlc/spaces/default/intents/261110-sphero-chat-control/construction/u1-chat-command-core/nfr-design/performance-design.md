# Performance Design — u1-chat-command-core

Grounded in NFR requirements [performance-requirements], functional design [functional-spec], contract design [contract-summary], security design [security-design], scalability design [scalability-design], reliability design [reliability-design], observability design [observability-design], logical components [logical-components], and tech stack decisions [tech-stack-decisions].

## NFR4 — Chat→Robot Latency Design

| ID | Requirement | Design Approach | Implementation |
|----|-------------|-----------------|----------------|
| NFR4.1 | Chat→robot command execution latency ≤ 5 seconds | Pipeline: chat input → validation → agent translation → Bluetooth LE command → robot motion. Each step measured for latency. | End-to-end timing instrumentation from chat message receipt to robot motion start. |
| NFR4.2 | Bluetooth LE command round-trip ≤ 500ms | Direct Bluetooth LE write with acknowledgment. | Single write operation with acknowledgment callback; no queuing or batching. |
| NFR4.3 | Agent response time ≤ 3 seconds | LangChain Deep Agents + OpenRouter with function calling for command extraction. | Single LLM call with function definitions for robot commands; no multi-turn conversation. |
| NFR4.4 | Retry vs. latency bound | Single retry with exponential backoff (initial delay 100ms, max delay 500ms); total retry budget within 500ms Bluetooth LE window. | Retry wrapper around Bluetooth LE write; exponential backoff jitter; error to chat UI if both attempts fail. |
| NFR4.5 | Latency risk - OpenRouter | Accepted risk: OpenRouter model latency outside team control; no SLA. | Documented as accepted risk with system owner; fallback to error message in chat UI if model times out. |

## Latency Budget Breakdown

| Component | Budget | Rationale |
|-----------|--------|-----------|
| Chat input validation | < 50ms | Simple string validation |
| Agent translation (Deep Agents + OpenRouter) | ≤ 3000ms | LLM inference time, outside team control |
| Command validation (against allowed vocabulary) | < 50ms | Simple string matching |
| Bluetooth LE write + acknowledgment | ≤ 500ms | Direct BLE write with ACK |
| Robot motion start | < 100ms | Sphero Mini internal processing |
| **Total budget** | **≤ 5000ms** | Within NFR4.1 target |

## Assumptions & Open Questions

None.
