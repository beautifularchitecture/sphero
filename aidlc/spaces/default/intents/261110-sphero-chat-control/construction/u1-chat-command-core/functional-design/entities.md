# Entity Model — u1-chat-command-core

Grounded in components [components], stories [stories], requirements [requirements], and unit-of-work [unit-of-work].

```yaml
entities:
  - name: ChatMessage
    description: >
      A chat message sent by the user through the web chat window, forwarded
      to the AgentCommand component for translation into robot commands.
    identifier: messageId
    attributes:
      - name: messageId
        logicalType: string
        required: true
        unique: true
        description: Unique identifier of the chat message
      - name: text
        logicalType: string
        required: true
        description: The raw text of the user's chat message
      - name: timestamp
        logicalType: datetime
        required: true
        description: ISO-8601 timestamp when the message was sent
      - name: direction
        logicalType: string
        required: true
        enum: [inbound, outbound]
        description: Direction of the message (inbound from user, outbound to user)
      - name: sender
        logicalType: string
        required: true
        enum: [user]
        description: Sender of the message (always "user" in this MVP)
      - name: messageType
        logicalType: string
        required: true
        enum: [command, query, status]
        description: Type of the message (command to robot, query for info, status check)
      - name: language
        logicalType: string
        required: false
        description: Natural language of the message text
    references: []
    entityLevelConstraints:
      - text must not be empty or whitespace-only
      - messageType must be one of command/query/status

  - name: RobotCommand
    description: >
      A robot command emitted by the AgentCommand component after translating
      a chat message, sent to the Sphero Mini over Bluetooth LE.
    identifier: commandId
    attributes:
      - name: commandId
        logicalType: string
        required: true
        unique: true
        description: Unique identifier of the robot command
      - name: command
        logicalType: string
        required: true
        enum: [forward, back, left, right, stop, setSpeed, setColor]
        description: The robot command to execute
      - name: speed
        logicalType: string
        required: false
        enum: [low, medium, high]
        description: Speed setting for movement commands
      - name: color
        logicalType: string
        required: false
        enum: [red, blue, green]
        description: LED color for color commands
      - name: timestamp
        logicalType: datetime
        required: true
        description: ISO-8601 timestamp when the command was emitted
      - name: status
        logicalType: string
        required: true
        enum: [moving, stopped, error]
        description: Execution status of the command (moving, stopped, error — matches Contract 1 CommandExecutionStatus)
      - name: source
        logicalType: string
        required: true
        enum: [chat, button, api]
        description: Origin of the command (chat message, UI button, external API)
      - name: retryCount
        logicalType: integer
        required: true
        default: 0
        description: Number of retry attempts for this command
    references: []
    entityLevelConstraints:
      - speed is required when command is a movement command
      - color is required when command is setColor

  - name: RobotState
    description: >
      The current state of the Sphero Mini robot, received via Bluetooth LE
      telemetry and published to the stats UI.
    identifier: stateId
    attributes:
      - name: stateId
        logicalType: string
        required: true
        unique: true
        description: Unique identifier of the robot state reading
      - name: direction
        logicalType: string
        required: true
        description: Robot direction (e.g., north, south, east, west)
      - name: orientation
        logicalType: number
        required: true
        description: Robot orientation in degrees
      - name: color
        logicalType: string
        required: true
        description: Current LED color (e.g., red, blue, green)
      - name: position
        logicalType: string
        required: true
        description: Robot position coordinates (e.g., "1.2, 0.4" meters)
      - name: timestamp
        logicalType: datetime
        required: true
        description: ISO-8601 timestamp of the telemetry reading
      - name: batteryLevel
        logicalType: number
        required: false
        description: Robot battery level percentage (0-100)
      - name: signalStrength
        logicalType: number
        required: false
        description: Bluetooth LE signal strength (RSSI in dBm)
    references: []
    entityLevelConstraints:
      - orientation must be in range [0, 360)
      - batteryLevel, when present, must be in range [0, 100]
```

## Entity Summary

| Entity | Owning Component | Identifier | Key Attributes | References |
|--------|-----------------|------------|----------------|------------|
| ChatMessage | ChatInput | messageId | text, timestamp, direction, sender, messageType, language | — |
| RobotCommand | RobotCommand | commandId | command, speed, color, timestamp, status, source, retryCount | — |
| RobotState | RobotTelemetry | stateId | direction, orientation, color, position, timestamp, batteryLevel, signalStrength | — |

## Relationships

- ChatMessage → RobotCommand: A chat message of type "command" may be translated into one RobotCommand (1:0..1)
- RobotCommand → RobotState: A robot command may produce a RobotState reading when executed (1:0..1)

## Assumptions & Open Questions

None.
