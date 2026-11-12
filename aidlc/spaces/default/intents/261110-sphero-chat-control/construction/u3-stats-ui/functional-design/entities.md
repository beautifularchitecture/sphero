# Entity Model — u3-stats-ui

Grounded in unit-of-work [unit-of-work], unit-of-work-story-map [unit-of-work-story-map], stories [stories], requirements [requirements], domain-design [components], contract-summary [contract-summary], and functional-design questions [functional-design-questions].

## Source of Truth

```yaml
entities:
  - name: RobotState
    identifier: stateId
    description: >
      Normalized robot telemetry state received from the Sphero Mini over
      Bluetooth LE via U2 RobotTelemetry. Represents the robot's current
      observable state at a point in time: direction, orientation, color,
      position, and when it was read. Produced by U2, consumed by U3 StatsDisplay.
    attributes:
      - name: stateId
        type: uuid
        required: true
        unique: true
        description: Unique identifier for this telemetry reading
        defaults: []
        constraints: []
      - name: direction
        type: string
        required: true
        unique: false
        description: Robot direction (e.g., north, south, forward, backward)
        allowed_values: [north, south, east, west, forward, backward, left, right, stationary]
        defaults: []
        constraints: []
      - name: orientation
        type: number
        required: true
        unique: false
        description: Robot orientation in degrees (0–359)
        allowed_values: []
        defaults: []
        constraints: [min: 0, max: 359]
      - name: color
        type: string
        required: true
        unique: false
        description: LED color (e.g., red, blue, green)
        allowed_values: [red, blue, green, yellow, cyan, magenta, white, off]
        defaults: []
        constraints: []
      - name: position
        type: string
        required: true
        unique: false
        description: Robot position coordinates (e.g., "1.2, 0.4")
        allowed_values: []
        defaults: []
        constraints: []
      - name: timestamp
        type: string
        required: true
        unique: false
        description: ISO-8601 timestamp of when the telemetry reading was received
        allowed_values: []
        defaults: []
        constraints: [format: date-time]
      - name: connectionStatus
        type: string
        required: true
        unique: false
        description: BLE connection state (connected, disconnected, pairing, error)
        allowed_values: [connected, disconnected, pairing, error]
        defaults: []
        constraints: []
    references:
      - component: RobotTelemetry
        unit: u2-telemetry
        relationship: produces
    entity_constraints:
      - id: ER1
        statement: >
          A RobotState may be published with partial attributes (missing fields
          filled with dash/null placeholders per U2 BR1.4.1 lenient normalization);
          all six attributes are expected when telemetry is complete.
      - id: ER2
        statement: >
          RobotState is append-only: each new reading creates a new stateId;
          states are not updated in place.
      - id: ER3
        statement: >
          connectionStatus is derived from U2's BLE connection state and U1's
          sync callback reporting; U3 does not independently determine it.
    relationships:
      - name: RobotState consumed by StatsDisplay
        from: RobotState
        to: StatsDisplay
        cardinality: many-to-one
        direction: from
  - name: ErrorMessage
    identifier: errorId
    description: >
      Error message displayed in the chat UI when the agent or backend
      encounters an error, Bluetooth permission is denied, or the robot
      disconnects. Produced by U1/U2 error reporting, consumed by U3 StatsDisplay.
    attributes:
      - name: errorId
        type: uuid
        required: true
        unique: true
        description: Unique identifier for this error
        defaults: []
        constraints: []
      - name: errorType
        type: string
        required: true
        unique: false
        description: Category of error (unrecognized-message, backend-error, bluetooth-error, disconnect)
        allowed_values: [unrecognized-message, backend-error, bluetooth-error, disconnect]
        defaults: []
        constraints: []
      - name: message
        type: string
        required: true
        unique: false
        description: Human-readable error message for the user
        allowed_values: []
        defaults: []
        constraints: []
      - name: timestamp
        type: string
        required: true
        unique: false
        description: ISO-8601 timestamp of when the error occurred
        allowed_values: []
        defaults: []
        constraints: [format: date-time]
    references: []
    entity_constraints:
      - id: ER4
        statement: >
          ErrorMessage is ephemeral: displayed once in the chat UI and not
          persisted beyond the session.
    relationships: []

## Entity Summary

| Entity | Identifier | Attributes | Key Constraints |
|--------|------------|------------|-----------------|
| RobotState | stateId | direction, orientation, color, position, timestamp, connectionStatus | Append-only (ER2); partial attributes allowed with dash/null placeholders (ER1); connectionStatus derived from U2/U1 (ER3) |
| ErrorMessage | errorId | errorType, message, timestamp | Ephemeral — displayed once, not persisted (ER4) |

## Relationships

- RobotState is produced by U2 RobotTelemetry and consumed by U3 StatsDisplay via Contract 2 events (robot.state.changed topic).
- ErrorMessage is produced by U1/U2 error reporting and displayed in U3's chat UI.

## Assumptions & Open Questions

None.
