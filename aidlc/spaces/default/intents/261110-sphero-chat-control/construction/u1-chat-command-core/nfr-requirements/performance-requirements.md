# Performance Requirements — u1-chat-command-core

Grounded in requirements analysis, functional design, and business rules.

## NFR4 — Chat→Robot Latency

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR4.1 | Chat→robot command execution latency | Robot motion begins within 5 seconds of a valid chat command being sent by the user | NFR4 |
| NFR4.5 | Latency risk | End-to-end latency depends on OpenRouter LLM inference (outside team control, no SLA); retry-once plus error reporting mitigates; accepted as a documented risk with owner = system owner | NFR4 |
| NFR4.2 | Bluetooth LE command round-trip | Command acknowledged by Sphero Mini within 500ms of being sent over Bluetooth LE | NFR4 |
| NFR4.3 | Agent response time | LangChain Deep Agents + OpenRouter returns a command within 3 seconds of receiving a validated chat message | NFR4 |
| NFR4.4 | Retry vs. latency bound | Retry once with backoff; end-to-end latency budget: chat message to robot motion ≤ 5 seconds (agent response ≤ 3s includes LLM inference; Bluetooth round-trip ≤ 500ms is within the 5s budget; if retry exceeds bound, report error to chat UI) | NFR4 |

## Assumptions & Open Questions

- Sphero Mini hardware is available and charged
- Linux machine with BlueZ and Bluetooth LE adapter is available
- OpenRouter API key is available and valid
- OpenRouter model responds within the 3-second target for NFR4.3
