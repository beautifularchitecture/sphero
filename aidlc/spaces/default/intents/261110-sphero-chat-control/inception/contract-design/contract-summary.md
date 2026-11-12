# Contract Summary — Sphero Mini Chat Control

Grounded in unit-of-work [unit-of-work], unit-of-work-dependency [unit-of-work-dependency], components [components], and requirements [requirements].

## Contracts Table

| # | Provider Unit | Consumer | Mechanism | Owner | Spec Format |
|---|--------------|----------|-----------|-------|-------------|
| 1 | U1 (u1-chat-command-core) | U2 (u2-telemetry) | Sync callback | U1 | Shared schema |
| 2 | U2 (u2-telemetry) | U3 (u3-stats-ui) | Event (publish/subscribe) | U2 | AsyncAPI |
| 3 | U1 (u1-chat-command-core) | External: OpenRouter API | Sync REST/HTTP | U1 | OpenAPI |

## Per-Contract Specifications

### Contract 1 — U1 → U2: Command Execution Status

**Provider:** U1 (u1-chat-command-core)  
**Consumer:** U2 (u2-telemetry)  
**Mechanism:** Sync callback (function call)  
**Owner:** U1  
**Format:** Shared schema

```yaml
shared-schema:
  name: CommandExecutionStatus
  version: "1.0.0"
  fields:
    - name: commandId
      type: string
      required: true
      description: Unique identifier of the robot command
    - name: status
      type: string
      required: true
      enum: [moving, stopped, error]
      description: Execution status of the command
    - name: timestamp
      type: string
      required: true
      format: date-time
      description: ISO-8601 timestamp of the status change
  error_handling:
    - condition: Sync callback returns error
      action: U1 (caller) retries once with backoff
    - condition: Callback unavailable
      action: U1 logs and continues; telemetry proceeds without status correlation
```

### Contract 2 — U2 → U3: RobotState Telemetry Events

**Provider:** U2 (u2-telemetry)  
**Consumer:** U3 (u3-stats-ui)  
**Mechanism:** Event (publish/subscribe)  
**Owner:** U2  
**Format:** AsyncAPI

```yaml
asyncapi:
  name: RobotStateTelemetry
  version: "1.0.0"
  topic: robot.state.changed
  protocol: event
  payload:
    - name: direction
      type: string
      required: false
      description: Robot direction (e.g., north, south)
    - name: orientation
      type: number
      required: false
      description: Robot orientation in degrees
    - name: color
      type: string
      required: false
      description: LED color (e.g., red, blue, green)
    - name: position
      type: string
      required: false
      description: Robot position coordinates (e.g., "1.2, 0.4")
    - name: timestamp
      type: string
      required: true
      format: date-time
      description: ISO-8601 timestamp of the telemetry reading
    - name: connectionStatus
      type: string
      required: false
      description: BLE connection state (connected, disconnected, pairing, error)
  error_handling:
    - condition: Event delivery fails
      action: Fire-and-forget; no retry; next event overwrites
    - condition: Consumer unavailable
      action: Event is dropped; consumer reconnects on next publish
```

### Contract 3 — U1 → OpenRouter API: Chat-to-Command Translation

**Provider:** External: OpenRouter API  
**Consumer:** U1 (u1-chat-command-core)  
**Mechanism:** Sync REST/HTTP  
**Owner:** U1  
**Format:** OpenAPI

```yaml
openapi:
  name: OpenRouterChatCompletion
  version: "1.0.0"
  endpoint: POST https://openrouter.ai/api/v1/chat/completions
  auth: Bearer token from .env (OPENROUTER_API_KEY)
  request:
    - name: model
      type: string
      required: true
      description: OpenRouter model identifier
    - name: messages
      type: array
      required: true
      description: Chat messages (system + user + assistant turns)
    - name: temperature
      type: number
      required: false
      description: Sampling temperature (default 0.7)
  response:
    - name: choices[].message.content
      type: string
      required: true
      description: Model response text containing robot command(s)
  error_handling:
    - condition: API returns error or timeout
      action: Retry up to 3 times with exponential backoff; on final failure, show error in chat UI
    - condition: API key missing or invalid
      action: Fail fast with chat UI error message
  security:
    - API key loaded from .env at startup; never committed to version control
    - API key never logged or shown in UI
```

## Contract Ownership Rules

| Contract | Owner | Breaking-Change Agreement | Additive Change Safety |
|----------|-------|---------------------------|------------------------|
| U1 → U2 CommandExecutionStatus | U1 | Breaking changes require U2's agreement | Consumers ignore unknown fields |
| U2 → U3 RobotStateTelemetry | U2 | Breaking changes require U3's agreement | Consumers ignore unknown fields |
| U1 → OpenRouter ChatCompletion | U1 | External API — U1 adapts to OpenRouter's versioning | U1 pins model version in config |

- Semantic versioning applied to each contract spec.
- Breaking changes require consumer agreement before deployment.
- Additive changes are safe: consumers ignore unknown fields.

## Open Questions

| Contract | Question | Blocks |
|----------|----------|--------|
| U1 → U2 | What happens if U2 is unavailable when U1's sync callback fires? Does U1 queue or drop the status? | U1 implementation |
| U2 → U3 | What is the event delivery guarantee (at-least-once, at-most-once, exactly-once)? | U3 event handling |
| U1 → OpenRouter | Which OpenRouter model ID is pinned in configuration? | U1 agent setup |

## Assumptions & Open Questions

See the Open Questions table above.
