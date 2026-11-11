# User Stories — Sphero Mini Chat Control

## Story Format

Standard: "As a [persona], I want [goal], so that [benefit]."  
Acceptance criteria in Given/When/Then (BDD) format, matching the team's affirmed BDD methodology. [team-practices] [Q1]

## Story P1 — Robot Operator

### US1.1 — Chat-driven robot movement

**As a** robot operator, **I want to** type a chat message like "roll forward" and have the Sphero Mini move accordingly, **so that** I can control the robot from a web interface.

**Priority:** Must Have  
**Breakdown:** By capability — movement  
**Source:** [FR1.1] [FR1]

**Acceptance Criteria:**
- **AC1.1.1:** Given the robot is connected and the chat UI is open, when I type "roll forward" and send it, then the robot moves forward.
- **AC1.1.2:** Given the robot is moving, when I type "stop" and send it, then the robot stops moving.
- **AC1.1.3:** Given the robot is idle, when I type "turn left" and send it, then the robot turns left.
- **AC1.1.4:** Given the robot is idle, when I type "turn right" and send it, then the robot turns right.
- **AC1.1.5:** Given I type "roll back" and send it, then the robot moves backward.

### US1.2 — Speed control

**As a** robot operator, **I want to** set the robot's speed (low, medium, high) through chat, **so that** I can control how fast the robot moves.

**Priority:** Could Have  
**Breakdown:** By capability — speed  
**Source:** [FR1.2] [Q5]

**Acceptance Criteria:**
- **AC1.2.1:** Given the robot is connected, when I type "set speed low" and send it, then subsequent movement commands use low speed.
- **AC1.2.2:** Given the robot is connected, when I type "set speed medium" and send it, then subsequent movement commands use medium speed.
- **AC1.2.3:** Given the robot is connected, when I type "set speed high" and send it, then subsequent movement commands use high speed.

### US1.3 — LED color control

**As a** robot operator, **I want to** change the Sphero Mini's LED color through chat, **so that** I can visually identify the robot's state.

**Priority:** Should Have  
**Breakdown:** By capability — color  
**Source:** [FR2] [Q4]

**Acceptance Criteria:**
- **AC1.3.1:** Given the robot is connected, when I type "set color red" and send it, then the robot's LED turns red.
- **AC1.3.2:** Given the robot is connected, when I type "set color blue" and send it, then the robot's LED turns blue.
- **AC1.3.3:** Given the robot is connected, when I type "set color green" and send it, then the robot's LED turns green.

### US1.4 — Stats panel observability

**As a** robot operator, **I want to** see the robot's direction, orientation, color, and position on a stats panel, **so that** I can observe what the robot is doing in real time.

**Priority:** Must Have  
**Breakdown:** By capability — observability  
**Source:** [NFR3] [Q4-Intent]

**Acceptance Criteria:**
- **AC1.4.1:** Given the robot is connected, when the robot's state changes, then the stats panel updates direction, orientation, color, and position on every robot state change.
- **AC1.4.2:** Given no robot is connected, then the stats panel shows a disconnected status.

### US1.5 — Error handling and rephrase

**As a** robot operator, **I want to** see an error message in the chat when my message is unclear or something fails, **so that** I know what went wrong and can rephrase.

**Priority:** Must Have  
**Breakdown:** By capability — error handling  
**Source:** [FR3] [FR4] [Q2] [Q5-Intent]

**Acceptance Criteria:**
- **AC1.5.1:** Given I type an unrecognized chat message, when I send it, then the system asks me to rephrase before taking any robot action.
- **AC1.5.2:** Given the agent or backend encounters an error, when the error occurs, then the robot stops and the error is shown in the chat UI.
- **AC1.5.3:** Given Bluetooth permission is denied, when the backend tries to connect, then the error is shown in the chat UI and the robot does not move.
- **AC1.5.4:** Given the robot disconnects mid-operation, when the disconnect occurs, then the error is shown in the chat UI and movement stops.

## INVEST Compliance Notes

| Story | Independent | Negotiable | Valuable | Estimable | Small | Testable |
|-------|-------------|------------|----------|-----------|-------|----------|
| US1.1 | Yes | Yes | Yes | Yes | Yes | Yes — AC1.1.1–AC1.1.5 |
| US1.2 | Yes | Yes | Yes | Yes | Yes | Yes — AC1.2.1–AC1.2.3 |
| US1.3 | Yes | Yes | Yes | Yes | Yes | Yes — AC1.3.1–AC1.3.3 |
| US1.4 | Yes | Yes | Yes | Yes | Yes | Yes — AC1.4.1–AC1.4.2 |
| US1.5 | Yes | Yes | Yes | Yes | Yes | Yes — AC1.5.1–AC1.5.4 |

## Dependencies

- US1.1 depends on the robot being connected (Bluetooth pairing handled at setup). [NFR2]
- US1.2 depends on US1.1 (movement must exist before speed can be applied).
- US1.3 is independent of US1.1/US1.2.
- US1.4 depends on robot telemetry being available (NFR3).
- US1.5 applies to all stories (error handling is cross-cutting).

## Assumptions & Open Questions

None.
