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
        enum: [user, agent]
        description: Sender of the message (user for inbound, agent for outbound responses)
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


```

## Entity Summary

| Entity | Owning Component | Identifier | Key Attributes | References |
|--------|-----------------|------------|----------------|------------|
| ChatMessage | ChatInput | messageId | text, timestamp, direction, sender, messageType, language | — |
| RobotCommand | RobotCommand | commandId | command, speed, color, timestamp, status, source, retryCount | — |


## Relationships

- ChatMessage → RobotCommand: A chat message of type "command" may be translated into one RobotCommand (1:0..1)


## Assumptions & Open Questions

None.
