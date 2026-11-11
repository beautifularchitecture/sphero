# Logical Components — u1-chat-command-core

Grounded in NFR requirements [nfr-requirements], functional design [functional-spec], and domain design [components.md].

## Component Decomposition

| Component | Responsibilities | NFR Coverage |
|-----------|-----------------|--------------|
| ChatInput | Accept chat input from user; validate non-empty, valid UTF-8, matches known command pattern; forward to AgentCommand; display agent responses and errors. | NFR9.1 (chat input validation), NFR9.3 (chat input authentication) |
| AgentCommand | Translate free-form chat into robot commands using LangChain Deep Agents + OpenRouter; validate commands against allowed vocabulary; request rephrase for unclear messages. | NFR4.1 (chat→robot latency), NFR4.3 (agent response time), NFR4.5 (latency risk), BR1.2 (command translation) |
| RobotCommand | Translate robot commands to Bluetooth LE commands; send to Sphero Mini; report execution status to RobotTelemetry. | NFR4.2 (Bluetooth LE round-trip), NFR4.4 (retry vs. latency), NFR2.1 (Bluetooth pairing), NFR2.2 (connection errors) |
| RobotTelemetry | Receive telemetry from Sphero Mini via Bluetooth LE; normalize into RobotState; publish state-change events. | NFR3.1 (stats panel data), NFR3.2 (connection status) |
| StatsDisplay | Render robot state on stats panel UI; subscribe to RobotState events; display connection status; inline speed/color selector buttons. | NFR3.1 (stats panel data), NFR3.2 (connection status), NFR3.3 (error visibility) |

## Component Interactions

```
ChatInput →(chat text) AgentCommand →(robot command) RobotCommand →(Bluetooth LE command) Sphero Mini
                                                      ↓
                                              RobotTelemetry ←(Bluetooth LE telemetry) Sphero Mini
                                                      ↓
                                              RobotState event → StatsDisplay
```

## External Dependencies

| Component | Dependency | Kind | Purpose |
|-----------|-----------|------|---------|
| AgentCommand | OpenRouter API | third-party-api | hosts LLM model for chat-to-command translation |
| RobotCommand | Sphero Mini Bluetooth LE | third-party-api | physical robot Bluetooth LE interface |
| RobotTelemetry | Sphero Mini Bluetooth LE | third-party-api | physical robot Bluetooth LE interface for telemetry |

## Assumptions & Open Questions

None.
