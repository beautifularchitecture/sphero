# Intent Backlog — Sphero Mini Chat Control

Grounded in the intent statement [intent-statement], feasibility assessment [feasibility-assessment], and constraint register [constraint-register]. Prioritized proto-Units for the MVP, using MoSCoW. Sequencing is value-first: chat → robot end-to-end as fast as possible, then polish stats. [Q4] [Q5]

## Must Have (MoSCoW: Must)

| ID | Proto-Unit | Description | Value | Source |
|----|-----------|-------------|-------|--------|
| U1 | Bluetooth robot connection | Pair once at setup; connect Sphero Mini via BlueZ + bleak/pygatt on Linux | Enables all robot motion | [Q1-Feas] [Q6-Intent] |
| U2 | Chat input endpoint | FastAPI websocket endpoint receiving user chat messages | Core user input path | [Q2-Feas] [Q1] |
| U3 | Agent command generation | LangChain Deep Agents + OpenRouter translates chat into robot commands | Core AI capability | [Q3-Feas] [Q4-Intent] |
| U4 | Robot command execution | Send movement (forward/back/left/right/stop), speed, LED color to the Sphero Mini | Core robot output | [Q1] [Q2-A,B,C] |
| U5 | Stats panel | React SPA showing direction, orientation, color, position, refreshed on every robot state change | Observability | [Q1] [Q2-D] [Q5-Feas] |
| U6 | Error UI | Show agent/backend/robot errors in the chat UI; stop robot on failure | Fail-safe behaviour | [Q2-E] [Q5-Intent] |

## Nice-to-Have (MoSCoW: Could)

| ID | Proto-Unit | Description | Value | Source |
|----|-----------|-------------|-------|--------|
| U7 | Heading/orientation command | Turn robot to a stated direction | Directional precision | [Q2-F] |
| U8 | Connection status indicator | Show Bluetooth/robot connection status in the UI | Diagnostics | [Q2-G] |

## Dependencies

No strong dependencies between proto-Units; all can be built in parallel. [Q3]

## Sequencing

Value-first: U2 → U3 → U4 → U5 as the core chat-to-robot end-to-end path, then U1 (Bluetooth connection) hardened in parallel, then U6 (error UI), then nice-to-haves U7, U8. [Q4] [Q5]

## Assumptions & Open Questions

None.
