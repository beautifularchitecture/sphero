# Unit of Work — Sphero Mini Chat Control

Grounded in components [components], decisions [decisions], requirements [requirements], and user stories [stories].

## Unit Definitions

| Unit ID | Directory | Components | Kind | Stories |
|---------|-----------|------------|------|---------|
| U1 | u1-chat-command-core | ChatInput, AgentCommand, RobotCommand | service | US1.1, US1.2, US1.3 |
| U2 | u2-telemetry | RobotTelemetry | service | US1.4 (telemetry reception) |
| U3 | u3-stats-ui | StatsDisplay | ui | US1.4 (stats UI rendering), US1.5 |

## Unit Responsibilities

### U1 — u1-chat-command-core (Walking Skeleton — service)

**Description:** The smallest working integrated slice: accepts chat input, translates it to robot commands via Deep Agents + OpenRouter, and sends commands to the Sphero Mini over Bluetooth LE. Exercises the chat → robot end-to-end integration path.

**Boundaries:** Receives chat text from the web UI input field; emits Bluetooth LE commands to the Sphero Mini; validates commands against the allowed vocabulary; handles unclear/unrecognized messages by requesting rephrase.

**Responsibilities:**
- Own ChatMessage entity lifecycle
- Validate non-empty chat input before forwarding
- Translate chat text to robot commands using Deep Agents + OpenRouter
- Validate commands against allowed vocabulary
- Translate robot commands to Bluetooth LE commands
- Send commands to the Sphero Mini over Bluetooth LE
- Report command execution status
- Handle Bluetooth connection errors and disconnections

**Deployment model:** Standalone service — runs as a deployed executable on the Linux host, listening on websockets for chat input and connecting to the Sphero Mini via Bluetooth LE.

**Complexity:** L (large) — AI model integration, Bluetooth LE communication, command validation, error handling.

**Implementation notes:**
- Walking skeleton: must exercise chat → robot end-to-end before later Units
- Depends on OpenRouter API key (.env, never committed)
- Depends on Sphero Mini Bluetooth LE pairing
- BDD acceptance criteria US1.1–US1.3

### U2 — u2-telemetry (service)

**Description:** Receives robot telemetry (direction, orientation, color, position) from the Sphero Mini over Bluetooth LE, normalizes it into RobotState, and publishes state-change events for the stats UI.

**Boundaries:** Listens for telemetry events from the Sphero Mini via Bluetooth LE; publishes RobotState events; reports command execution status from U1.

**Responsibilities:**
- Receive telemetry events from the Sphero Mini over Bluetooth LE
- Normalize telemetry into RobotState entity (direction, orientation, color, position, timestamp)
- Publish RobotState changes as events
- Handle telemetry connection errors and disconnections
- Report command execution status received from U1

**Deployment model:** Standalone service — runs as a deployed executable on the Linux host, connecting to the Sphero Mini via Bluetooth LE.

**Complexity:** M (medium) — Bluetooth LE telemetry reception, event publishing, error handling.

**Implementation notes:**
- Depends on U1's command execution status reporting
- Owns RobotState entity
- BDD acceptance criteria US1.4 (telemetry reception part)

### U3 — u3-stats-ui (ui)

**Description:** Renders the robot's current state (direction, orientation, color, position) and connection status on the stats panel of the SPA. Subscribes to RobotState events from U2 and updates the UI in real time.

**Boundaries:** Subscribes to RobotState events; renders stats panel; displays connection status; handles partial telemetry.

**Responsibilities:**
- Subscribe to RobotState events from U2
- Update stats panel UI with current direction, orientation, color, position
- Display connection status (connected, disconnected, pairing, error)
- Handle partial telemetry (missing fields shown as dashes)
- Render inline speed/color selector buttons alongside chat input

**Deployment model:** Embedded — served as part of the FastAPI backend's static frontend, deployed with U1's service instance but maintainable as a separate UI artifact.

**Complexity:** M (medium) — React SPA, websocket client for telemetry events, inline UI controls.

**Implementation notes:**
- Depends on U2's telemetry event format
- Inline speed/color selector buttons (from Units Generation Q2 answer)
- BDD acceptance criteria US1.4 (stats UI part), US1.5

## Assumptions & Open Questions

None.
