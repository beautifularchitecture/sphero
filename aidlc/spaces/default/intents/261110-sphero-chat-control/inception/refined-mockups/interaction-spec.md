# Interaction Specification — Sphero Mini Chat Control

## Interaction Patterns

### Pattern: Chat input with inline selectors

**Trigger:** User opens the chat window on the main screen.

**Behavior:**
1. User types a chat message (e.g., "roll forward") into the message input field.
2. User presses Send (or Enter key) — the message is sent to the backend over websocket.
3. The agent translates the message into a robot command and emits it.
4. The command is sent to the Sphero Mini over Bluetooth LE; the robot begins moving.
5. Robot telemetry (direction, orientation, color, position) is sent to the backend and updates the stats panel live.

**Keyboard:**
- Tab into message input field
- Type message
- Enter to send (primary action)
- Escape to clear the input field

**Source:** [user-flow] [FR1.1] [FR1.2] [FR2]

### Pattern: Inline speed selector

**Trigger:** User wants to set robot speed (low/medium/high).

**Behavior:**
1. User clicks or tabs to a speed button (Low / Medium / High).
2. The selected button is highlighted; the others are unselected.
3. The speed setting applies to subsequent movement commands.
4. A chat message "set speed <level>" is also posted to the chat window for the agent to process.

**Keyboard:**
- Arrow keys to move between speed options
- Enter/Space to select

**Source:** [Q2] [FR1.2] [US1.2]

### Pattern: Inline color selector

**Trigger:** User wants to change the robot's LED color.

**Behavior:**
1. User clicks or tabs to a color button (red / blue / green).
2. The selected button is highlighted.
3. A chat message "set color <color>" is posted to the chat window for the agent to process.

**Keyboard:**
- Arrow keys to move between color options
- Enter/Space to select

**Source:** [Q2] [FR2] [US1.3]

### Pattern: Pairing modal

**Trigger:** First-time use or when the robot is disconnected and the user initiates pairing.

**Behavior:**
1. A modal opens with pairing instructions.
2. User puts the Sphero Mini into pairing mode.
3. Backend discovers the robot over Bluetooth LE and pairs.
4. On success, the modal closes and the screen transitions to the success state (robot connected).
5. On failure, an error message in the modal explains what went wrong and offers retry.

**Keyboard:**
- Tab to focus modal controls
- Enter/Space to activate
- Escape to close (if not a critical confirmation)

**Source:** [user-flow] [NFR2] [US1.5 AC1.5.3]

### Pattern: Error handling

**Trigger:** Agent uncertain, backend error, Bluetooth permission denied, robot disconnects mid-operation.

**Behavior:**
1. Robot stops moving immediately.
2. Error banner appears in the chat UI with a plain-language message.
3. Connection status indicator shows "disconnected" or "error."
4. Recovery action is suggested (retry, rephrase, check Bluetooth, check `.env` API key).

**Source:** [user-flow] [FR3] [FR4] [US1.5]

## State Transitions

| From | To | Trigger | Source |
|------|----|---------|--------|
| Empty (disconnected) | Loading | User initiates pairing | [user-flow] |
| Loading | Success | Pairing succeeds | [user-flow] |
| Loading | Error | Pairing fails | [user-flow] |
| Success | Error | Bluetooth/API error occurs | [user-flow] |
| Success | Empty | Robot disconnects | [user-flow] |

## Assumptions & Open Questions

None.
