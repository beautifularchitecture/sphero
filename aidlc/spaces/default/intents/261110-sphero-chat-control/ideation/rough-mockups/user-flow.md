# User Flow — Sphero Mini Chat Control

## Flow: Chat-to-Robot Control (Happy Path)

**Persona:** The user (single operator, own machine)  
**Trigger:** User opens the local website in a browser  
**Source:** [Q2] [Q1]

```
Steps:
  1. Main screen -> User types a chat message (e.g. "roll forward") -> Message appears in chat window
  2. Main screen -> User presses Send -> Message sent to backend over websocket
  3. Backend -> Agent translates message into robot command -> Command emitted (e.g. MOVE_FORWARD)
  4. Backend -> Command sent to Sphero Mini over Bluetooth LE -> Robot begins moving
  5. Robot -> Telemetry (direction, orientation, color, position) sent to backend -> Stats panel updates live
  6. Main screen -> User sees robot move and stats update -> Flow complete
```

**Success outcome:** Robot moves as instructed and stats panel reflects current robot state. [Q2]

## Error Paths

| Condition | Error screen/message | Recovery action | Source |
|-----------|---------------------|-----------------|--------|
| Agent uncertain or fails | Error banner in chat UI; robot stops | User retries or corrects message | [Q5-Intent] |
| Bluetooth/robot disconnected | Status indicator shows "disconnected" | User pairs/reconnects robot | [Q1-Feas] |
| Websocket connection drops | Status indicator shows "disconnected" | Frontend reconnects automatically | [Q2-Feas] |
| OpenRouter API error | Error message in chat UI | User checks `.env` API key | [Q4-Feas] |

## Assumptions & Open Questions

None.
