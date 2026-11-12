# Business Rules — u3-stats-ui

Grounded in unit-of-work [unit-of-work], unit-of-work-story-map [unit-of-work-story-map], stories [stories], requirements [requirements], domain-design [components], contract-summary [contract-summary], and functional-design questions [functional-design-questions].

## Source of Truth

```yaml
rules:
  - id: BR1.5.1
    statement: >
      U3 StatsDisplay shall render the robot's current state (direction,
      orientation, color, position) on the stats panel, updated on every
      RobotStateChanged event received from U2.
    category: policy
    applies_to: StatsDisplay
    trigger: RobotStateChanged event received on robot.state.changed topic
    logic: >
      IF a RobotStateChanged event arrives on robot.state.changed THEN update
      the stats panel with direction, orientation, color, position, and
      timestamp from the event payload.
    violation_behaviour: >
      Stats panel shows stale or missing values; user cannot observe robot state.
    source: [US1.4, AC1.4.1, NFR3]
  - id: BR1.5.2
    statement: >
      U3 StatsDisplay shall show the robot's BLE connection status
      (connected, disconnected, pairing, error) on the stats panel.
    category: constraint
    applies_to: StatsDisplay
    trigger: Connection state change reported by U2 or U1
    logic: >
      IF connection state changes THEN display the new status
      (connected, disconnected, pairing, or error) on the stats panel.
    violation_behaviour: >
      User cannot tell whether the robot is connected; stats panel may show
      stale state while disconnected.
    source: [US1.4, AC1.4.2]
  - id: BR1.5.3
    statement: >
      U3 StatsDisplay shall render missing RobotState fields as dashes
      (partial telemetry tolerance per U2 BR1.4.1 lenient normalization).
    category: validation
    applies_to: StatsDisplay
    trigger: RobotState with missing or null attributes received
    logic: >
      IF any RobotState attribute is missing or null THEN render it as a dash
      ("-") instead of omitting or blocking the update.
    violation_behaviour: >
      Incomplete telemetry blocks the stats panel update; user sees no state.
    source: [US1.4, ER1, BR1.4.1]
  - id: BR1.5.4
    statement: >
      U3 StatsDisplay shall display error messages in the chat UI when the
      agent or backend encounters an error, Bluetooth permission is denied,
      or the robot disconnects.
    category: constraint
    applies_to: ErrorMessage component
    trigger: Error reported by U1 or U2 (unrecognized message, backend error,
      Bluetooth error, disconnect)
    logic: >
      IF an error is reported THEN show an ErrorMessage component in the chat
      UI with the error type, message, and timestamp.
    violation_behaviour: >
      User is not informed of failures; unclear messages are not rephrased.
    source: [US1.5, AC1.5.1–AC1.5.4]
  - id: BR1.5.5
    statement: >
      U3 StatsDisplay shall provide inline speed/color selector buttons that
      send chat commands through the existing chat input path to U1.
    category: policy
    applies_to: SpeedColorSelector component
    trigger: User clicks a speed or color selector button
    logic: >
      IF a speed button is clicked THEN send "set speed <level>" as a chat
      message to U1; IF a color button is clicked THEN send "set color <color>"
      as a chat message to U1.
    violation_behaviour: >
      Speed and color cannot be controlled from the stats panel UI.
    source: [US1.2, US1.3, AC1.2.1–AC1.2.3, AC1.3.1–AC1.3.3]

## Rules Summary

| Rule ID | Category | Applies To | Trigger | Statement (abridged) |
|---------|----------|------------|---------|----------------------|
| BR1.5.1 | policy | StatsDisplay | RobotStateChanged event | Render robot state on stats panel, updated on every state change |
| BR1.5.2 | constraint | StatsDisplay | Connection state change | Show BLE connection status (connected/disconnected/pairing/error) |
| BR1.5.3 | validation | StatsDisplay | RobotState with missing attributes | Render missing fields as dashes (partial telemetry tolerance) |
| BR1.5.4 | constraint | ErrorMessage | Error reported by U1/U2 | Display error messages in the chat UI |
| BR1.5.5 | policy | SpeedColorSelector | Button click | Send speed/color chat commands to U1 via existing chat path |

## Assumptions & Open Questions

None.
