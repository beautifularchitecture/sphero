# Business Rules — u1-chat-command-core

Grounded in requirements [requirements], stories [stories], and unit-of-work [unit-of-work].

```yaml
rules:
  - id: BR1.1
    statement: >
      A chat message must be non-empty, not whitespace-only, valid UTF-8,
      and match a known command pattern (forward/back/left/right/stop,
      set speed, set color) before it is translated into a robot command.
    category: validation
    appliesTo: ChatMessage → RobotCommand translation
    trigger: User sends a chat message
    logic: >
      IF message is empty OR whitespace-only OR invalid UTF-8
      THEN reject with "please rephrase"
      IF message does not match a known command pattern
      THEN request user to rephrase
      ELSE translate message into robot command
    violationBehaviour: >
      The robot does not move; the chat UI shows a rephrase request.
    source: FR3, FR4

  - id: BR1.2
    statement: >
      The agent translates free-form chat into robot commands using the
      allowed vocabulary: forward, back, left, right, stop, setSpeed,
      setColor. Movement commands may carry a speed setting; color
      commands carry a color value.
    category: calculation
    appliesTo: AgentCommand
    trigger: Validated chat message received from ChatInput
    logic: >
      IF message is a movement request (forward/back/left/right/stop)
      THEN emit RobotCommand with command=movement and optional speed
      IF message is a color request (set color)
      THEN emit RobotCommand with command=setColor and color value
      IF message is a speed request (set speed)
      THEN emit RobotCommand with command=setSpeed and speed value
    violationBehaviour: >
      If no valid command can be determined, fall back to BR1.1
      (request rephrase).
    source: FR1.1, FR1.2, FR2

  - id: BR1.3
    statement: >
      When the agent or backend encounters an error or uncertainty, the
      robot stops and the error is shown in the chat UI. Unclear or
      unrecognized messages trigger a rephrase request before any
      robot action.
    category: policy
    appliesTo: All components (ChatInput, AgentCommand, RobotCommand)
    trigger: Error or uncertainty encountered during chat-to-command flow
    logic: >
      IF agent uncertainty OR backend error OR Bluetooth error
      THEN stop robot, show error in chat UI, await user rephrase or retry
    violationBehaviour: >
      Robot continues moving despite error state (unsafe).
    source: FR3, FR4

  - id: BR1.4
    statement: >
      Robot command execution status (moving/stopped/error) is reported
      from RobotCommand (U1) to RobotTelemetry (U2) via sync callback.
      If U2's callback is unavailable, U1 retries once with backoff;
      if still unavailable, U1 logs and continues without blocking.
    category: constraint
    appliesTo: RobotCommand → RobotTelemetry
    trigger: Robot command execution state change
    logic: >
      IF command execution state changes
      THEN report CommandExecutionStatus (commandId, status, timestamp)
      to RobotTelemetry via sync callback
      IF callback unavailable
      THEN retry once with backoff
      IF still unavailable
      THEN log and continue without blocking
    violationBehaviour: >
      Command status is not visible to the telemetry layer; stats UI
      cannot correlate commands with robot state.
    source: NFR3


```

## Rules Summary

| Rule ID | Category | Applies To | Trigger | Source |
|---------|----------|------------|---------|--------|
| BR1.1 | validation | ChatMessage → RobotCommand | User sends chat message | FR3, FR4 |
| BR1.2 | calculation | AgentCommand | Validated chat message | FR1.1, FR1.2, FR2 |
| BR1.3 | policy | All components | Error or uncertainty | FR3, FR4 |
| BR1.4 | constraint | RobotCommand → RobotTelemetry | Command execution state change | NFR3 |


## Assumptions & Open Questions

None.
