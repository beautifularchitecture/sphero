# Feasibility Assessment — Sphero Mini Chat Control

Grounded in intent statement [intent-statement] and answers [Q1]–[Q7].

## Technical Viability

**Verdict: Feasible.** No technical blockers identified for an MVP on a single Linux machine with local Bluetooth LE and LAN-only networking.

### Robot Connection (Q1)

The Sphero Mini (original) connects via Bluetooth LE using BlueZ with a Python library such as `bleak` or `pygatt`. Pairing is handled once at setup. [Q1] This is well-supported on Linux.

### Backend Tech Stack (Q2)

FastAPI with websockets provides the chat API and WebSocket server for real-time chat input and telemetry streaming. React SPA serves as the frontend, served by FastAPI static file serving or a separate dev server during development. [Q2]

### Agent Setup (Q3)

LangChain Deep Agents package directly, backed by an OpenRouter chat model, translates free-form chat into robot commands. [Q3]

### API Key Management (Q4)

OpenRouter API key stored in `.env` at project root, loaded at backend startup, never committed to version control. [Q4]

### Stats Observability (Q5)

SPA stats panel shows direction, orientation, color, and position, refreshed on every robot state change via websocket telemetry. [Q5]

### Failure Behaviour (Q5-Intent)

When the agent is uncertain or something fails (unclear chat, OpenRouter error, Bluetooth dropout), the robot stops and the error is shown in the chat UI. [Q5-Intent]

## Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-01 | Backend runs on Linux | [Q6] |
| C-02 | Robot connection via BlueZ + Python Bluetooth LE library | [Q1] |
| C-03 | Pairing handled once at setup | [Q1] |
| C-04 | Backend tech stack: FastAPI + websockets | [Q2] |
| C-05 | Frontend: React SPA served by backend | [Q2] |
| C-06 | Agent: LangChain Deep Agents package directly | [Q3] |
| C-07 | Model: OpenRouter chat model behind Deep Agents | [Q3] |
| C-08 | OpenRouter API key in `.env` at project root, never committed | [Q4] |
| C-09 | Stats panel shows direction, orientation, color, position | [Q5] |
| C-10 | Stats refreshed on every robot state change | [Q5] |
| C-11 | LAN-only access; no cloud or outside-network exposure | [Q8] |

## Out of Scope

| ID | Item | Reason | Source |
|----|------|--------|--------|
| OS-01 | Autonomous navigation or obstacle avoidance | MVP boundary | [Q8] |
| OS-02 | Multi-robot support | MVP boundary | [Q8] |
| OS-03 | Cloud hosting or outside-LAN access | MVP boundary | [Q8] |

## Risks

| ID | Risk | Likelihood | Impact | Mitigation | Source |
|----|------|------------|--------|------------|--------|
| R-01 | Bluetooth LE pairing/connection instability on Linux | Medium | High | Pair once at setup; show connection status in UI; retry with clear error | [Q1] |
| R-02 | OpenRouter model produces unclear or unsafe robot commands | Medium | Medium | Stop robot and show error in UI on uncertainty or failure | [Q3] [Q5] |
| R-03 | Websocket connection drops between frontend and backend | Low | Medium | Reconnect on frontend; show connection status | [Q2] |
| R-04 | API key exposure if `.env` is committed | Low | High | `.env` in `.gitignore`; never commit; load at startup only | [Q4] |

## Assumptions

| ID | Assumption | Basis | Source |
|----|------------|-------|--------|
| A-01 | Sphero Mini (original) is supported by BlueZ + bleak/pygatt on Linux | User-selected platform | [Q6] [Q1] |
| A-02 | LangChain Deep Agents package supports OpenRouter model integration | User-selected stack | [Q3] |
| A-03 | No compliance obligations for personal home-LAN project | User-selected context | [Q7] |

## Open Questions

None.

## Conclusion

Feasible. No technical blockers identified for an MVP on a single Linux machine with local Bluetooth LE and LAN-only networking. [Q1] [Q6] [Q7]