# Functional Design Questions — u1-chat-command-core

## Unit Context

Unit U1 (u1-chat-command-core) — service — chat input, AI translation via Deep Agents + OpenRouter, Bluetooth LE command sending — stories US1.1, US1.2, US1.3 — Complexity: L — Walking skeleton.

This unit is the walking skeleton: chat → robot end-to-end, exercising chat input, AI translation, Bluetooth LE command sending, and robot movement.

## Sources

- [unit-of-work] — units-generation/unit-of-work.md
- [unit-of-work-story-map] — units-generation/unit-of-work-story-map.md
- [stories] — user-stories/stories.md
- [requirements] — requirements-analysis/requirements.md
- [components] — domain-design/components.md
- [contract-summary] — contract-design/contract-summary.md

## Q1. [Product] Entity model — ChatMessage

The ChatMessage entity is owned by ChatInput. What attributes does it have beyond messageId, text, timestamp, and direction?

- A. Just those four attributes (messageId, text, timestamp, direction)
- B. Add: sender (always "user"), messageType (command/query/status), language
- C. Add: rawInput (the exact user text), normalizedText (cleaned for the agent), confidence (agent's confidence score)
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q2. [Product] Entity model — RobotCommand

The RobotCommand entity is owned by RobotCommand component. What attributes does it have?

- A. commandId, command, speed, color, timestamp, status
- B. commandId, command, speed, color, timestamp, status, source (chat/button/api), retryCount
- C. commandId, command, speed, color, timestamp, status, executionTimeMs
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q3. [Product] Entity model — RobotState

The RobotState entity is owned by RobotTelemetry. What attributes does it have?

- A. stateId, direction, orientation, color, position, timestamp
- B. stateId, direction, orientation, color, position, timestamp, batteryLevel, signalStrength
- C. stateId, direction, orientation, color, position, timestamp, lastCommandId
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q4. [Product] Business rules — Chat input validation

What rules apply when a user sends a chat message?

- A. Message must be non-empty; must be under 500 characters; must be valid UTF-8
- B. Message must be non-empty; no length limit; must not contain only whitespace
- C. Message must be non-empty; must match a known command pattern (forward/back/left/right/stop/set speed/set color); otherwise trigger rephrase
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q5. [Product] Business rules — Command translation

How does the agent translate chat into robot commands?

- A. Free-form: the agent decides any command from the user's words (confirmed at feasibility Q4)
- B. Fixed vocabulary: only forward/back/left/right/stop, set speed, set color
- C. Hybrid: free-form input but agent may only emit commands from the fixed vocabulary
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q6. [Product] Business rules — Error handling

What happens when the agent receives an unclear message?

- A. Ask the user to rephrase before taking any robot action (confirmed at feasibility Q5)
- B. Stop the robot and show the error in the UI
- C. Ignore the message and keep the last safe state
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q7. [Product] Data flow — Chat to command

Describe the step sequence when a user sends a chat message.

- A. User types → message validated → sent to backend → agent translates → command validated → sent to robot via Bluetooth → robot moves → telemetry updates stats
- B. User types → message sent to backend → agent translates → command sent to robot → robot moves (no validation step)
- C. User types → message validated → sent to backend → agent translates → command sent to robot → telemetry updates (no validation step)
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q8. [Product] Frontend components — Chat window

What components make up the chat window?

- A. Message list, message input, Send button (confirmed at refined mockups)
- B. Message list, message input, Send button, connection status indicator, speed selector, color selector
- C. Message list, message input, Send button, error banner, typing indicator
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q9. [Product] Frontend components — Stats panel

What components make up the stats panel?

- A. Direction, orientation, color, position, connection status (confirmed at refined mockups)
- B. Direction, orientation, color, position, connection status, battery level, signal strength
- C. Direction, orientation, color, position, connection status, last command, command history
- D. Not yet defined
- X. Other (please specify)

[Answer]:
