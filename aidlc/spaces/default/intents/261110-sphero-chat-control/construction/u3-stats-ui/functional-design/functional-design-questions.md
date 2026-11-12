# Functional Design Questions — u3-stats-ui

Grounded in unit-of-work [unit-of-work], unit-of-work-story-map [unit-of-work-story-map], stories [stories], requirements [requirements], domain-design [components], contract-summary [contract-summary].

## Q1. [Frontend] Stats panel component hierarchy

US1.4 requires the stats panel to show direction, orientation, color, position, refreshed on every robot state change. US1.5 requires error display and connection status. How should the frontend components be organized?

- A. Single StatsPanel component owns all rendering (direction, orientation, color, position, connection status, error messages)
- B. Split into StatsPanel (robot state values), ConnectionStatus indicator, ErrorMessage display, SpeedColorSelector buttons
- C. Not yet defined
- X. Other (please specify)

[Answer]: B

## Q2. [Integration] Telemetry event subscription

U2 publishes RobotStateChanged events on `robot.state.changed` per Contract 2 (fire-and-forget, WebSocket). How should U3 subscribe to these events?

- A. WebSocket client connecting to U2's `/ws/robot-state` endpoint, subscribing to robot.state.changed topic
- B. Polling endpoint on U2 for latest RobotState
- C. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q3. [Business rules] Connection status and partial telemetry

US1.4 AC1.4.2 requires showing disconnected status when no robot is connected. US1.4/ER1 allows partial telemetry (missing fields as dash/null). How should U3 handle these?

- A. Connection status indicator (connected/disconnected/pairing/error) + render missing fields as dashes in the stats panel
- B. Only show connected state; hide stats panel when disconnected; block on missing fields
- C. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q4. [Business rules] Speed/color selector buttons

US1.2/US1.3 support inline speed/color selector buttons alongside chat input. How should these buttons work?

- A. Buttons send chat commands ("set speed low/medium/high", "set color red/blue/green") through the existing chat input path to U1
- B. Buttons call a separate API endpoint on U1 for speed/color
- C. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q5. [Error handling] Error message display

US1.5 requires error messages in the chat UI when messages are unclear or failures occur. How should U3 display errors?

- A. Dedicated ErrorMessage component below the chat input, showing robot stop errors, BLE errors, and unclear-message rephrase requests
- B. Inline error text within the chat message list
- C. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q6. [Data flow] RobotState rendering

U2 publishes RobotState (direction, orientation, color, position, timestamp) per Contract 2. How should U3 render each attribute?

- A. Direction as compass text, orientation as degrees, color as colored swatch, position as coordinates, timestamp as last-update time
- B. All attributes as raw text values
- C. Not yet defined
- X. Other (please specify)

[Answer]: A
