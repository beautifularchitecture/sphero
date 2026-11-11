# Requirements Analysis — Sphero Mini Chat Control

## Intent Analysis

The user wants to control a Sphero Mini robot by typing chat messages into a local website, with the robot translating those messages into movement and other actions. The website runs on the local network only, and chat input goes to a Python backend that uses LangChain Deep Agents with an OpenRouter model to turn natural language into robot instructions. [desc] [Q1] [intent-statement]

The target customer is the user themselves, on their own machine, with no reporting or collaborators needed in this first version. [Q2] [intent-statement]

## Functional Requirements

| ID | Requirement | Source |
|----|-------------|--------|
| FR1 | The system shall accept chat messages from the user through a web chat window and forward them to the backend agent. | [desc] [intent-statement] [Q1-Intent] |
| FR1.1 | The system shall translate free-form chat into robot commands: forward, back, left, right, stop. | [desc] [intent-statement] [Q1-Intent] [Q1] |
| FR1.2 | The system shall support speed control at low, medium, and high settings for robot movement. | [Q1] |
| FR2 | The system shall control the Sphero Mini LED color through chat commands. | [desc] [intent-statement] [Q3-Intent] |
| FR3 | When the agent receives an unclear or unrecognized chat message, it shall ask the user to rephrase before taking any robot action. | [Q2] |
| FR4 | When the agent or backend encounters an error or uncertainty, it shall stop the robot and show the error in the chat UI. | [desc] [intent-statement] [Q5-Intent] [Q5] |

## Non-Functional Requirements

| ID | Requirement | Source |
|----|-------------|--------|
| NFR1 | The system shall run on the local network only; no cloud hosting or access from outside the LAN. | [desc] [intent-statement] [Q8-Intent] [TC-11] |
| NFR2 | The backend shall run on Linux and connect to the Sphero Mini (original) via BlueZ + a Python Bluetooth LE library (bleak/pygatt). | [desc] [intent-statement] [Q6-Intent] [TC-01] [Q1-Feas] |
| NFR3 | The SPA stats panel shall show direction, orientation, color, and position, refreshed on every robot state change. | [desc] [intent-statement] [Q5-Intent] [Q4] |
| NFR4 | No specific timing target is set for chat→robot latency; "works reliably on the LAN" is the success criterion. | [Q3] [Q7-Intent] |
| NFR5 | No formal accessibility (WCAG) requirement; keep the UI usable but do not certify. | [Q5] |
| NFR6 | The Python backend shall use pytest + coverage.py for testing; the React SPA shall use Vitest + React Testing Library. | [Q6] [Q7] |
| NFR7 | Test coverage shall meet an 80% line-coverage floor and tests shall run in CI before merge; failure blocks merge. | [team-practices] [scope-document] |
| NFR8 | Test methodology is BDD (Given/When/Then scenarios first, then implement, then run tests). | [team-practices] |

## Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| C-01 | No autonomous navigation or obstacle avoidance in this MVP. | [desc] [intent-statement] [Q8] [scope-document] |
| C-02 | No multi-robot support in this MVP. | [desc] [intent-statement] [Q8] [scope-document] |
| C-03 | No cloud hosting or access from outside the local network. | [desc] [intent-statement] [Q8] [TC-11] |
| C-04 | The OpenRouter API key shall be stored in `.env` at project root and never committed to version control. | [desc] [intent-statement] [Q4-Feas] [Q6] [team-practices] [project.md] |
| C-05 | The walking skeleton (chat → robot → stats end-to-end) shall be built first before additional features. | [team-practices] |

## Assumptions

| ID | Assumption | Rationale | Source |
|----|-----------|-----------|--------|
| A-01 | The Sphero Mini (original) is supported by BlueZ + bleak/pygatt on Linux. | User-selected platform; no evidence of incompatibility. | [Q6-Intent] [Q1-Feas] |
| A-02 | LangChain Deep Agents package supports OpenRouter model integration for translating chat to robot commands. | User-selected stack; no evidence of incompatibility. | [Q3-Feas] |
| A-03 | No compliance obligations apply to this personal home-LAN project. | User-confirmed context. | [Q7-Feas] [RC-01] |

## Out of Scope

| ID | Item | Reason | Source |
|----|------|--------|--------|
| OS-01 | Autonomous navigation or obstacle avoidance | MVP boundary | [Q8] [scope-document] |
| OS-02 | Multi-robot support | MVP boundary | [Q8] [scope-document] |
| OS-03 | Cloud hosting or outside-LAN access | MVP boundary | [Q8] [TC-11] |

## Open Questions

| ID | Question | Source |
|----|----------|--------|
| OQ-01 | Frontend test runner confirmed as Vitest + React Testing Library; revisit if the frontend stack changes. | [Q7] |

## Assumptions & Open Questions

See the tables above. No unresolved items beyond OQ-01.
