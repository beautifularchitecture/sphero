# Entity Model — u2-telemetry

Grounded in unit-of-work [unit-of-work], components [components], requirements [requirements], and contract-summary [contract-summary].

## Source of Truth

```yaml
entities:
  - name: RobotState
    identifier: stateId
    description: >
      Normalized robot telemetry state received from the Sphero Mini over
      Bluetooth LE. Represents the robot's current observable state at a
      point in time: direction, orientation, color, position, and when it
      was read.
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
    references: []
    entity_constraints:
      - id: ER1
        statement: >
          A RobotState may be published with partial attributes (missing fields
          filled with dash/null placeholders per BR1.4.1 lenient normalization);
          all five attributes are expected when telemetry is complete.
      - id: ER2
        statement: >
          RobotState is append-only: each new reading creates a new stateId;
          states are not updated in place.
    relationships:
      - name: RobotState produced by RobotTelemetry
        from: RobotState
        to: RobotTelemetry
        cardinality: many-to-one
        direction: from
      - name: RobotState consumed by StatsDisplay
        from: RobotState
        to: StatsDisplay
        cardinality: many-to-one
        direction: from
```

## Entity Summary

| Entity | Identifier | Owning Component | Attributes | Key Constraints |
|--------|------------|------------------|------------|-----------------|
| RobotState | stateId | RobotTelemetry (U2) | direction, orientation, color, position, timestamp | All five attributes present at publish time; missing field values may be dash/null placeholders per ER1/BR1.4.1 lenient normalization |

**RobotState** is the single entity owned by U2. It represents normalized robot telemetry received from the Sphero Mini over Bluetooth LE, produced by RobotTelemetry and consumed by StatsDisplay (U3) via Contract 2 events. Each reading generates a new stateId; states are append-only and never updated in place.