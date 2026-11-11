# Constraint Register — Sphero Mini Chat Control

Grounded in intent statement [intent-statement] and answers [Q1]–[Q7].

## Technical Constraints

| ID | Constraint | Scope | Source |
|----|------------|-------|--------|
| C-01 | Backend must run on Linux | Entire backend | [Q6] |
| C-02 | Robot connection via BlueZ + Python Bluetooth LE library (bleak/pygatt) | Bluetooth adapter | [Q1] |
| C-03 | Pairing handled once at setup | Bluetooth adapter | [Q1] |
| C-04 | Backend tech stack: FastAPI + websockets | Backend | [Q2] |
| C-05 | Frontend: React SPA served by backend | Frontend | [Q2] |
| C-06 | Agent: LangChain Deep Agents package directly | Backend agent | [Q3] |
| C-07 | Model: OpenRouter chat model behind Deep Agents | Backend agent | [Q3] |
| C-08 | OpenRouter API key in `.env` at project root, never committed | Configuration | [Q4] |
| C-09 | Stats panel shows direction, orientation, color, position | Frontend stats | [Q5] |
| C-10 | Stats refreshed on every robot state change | Frontend stats | [Q5] |
| C-11 | LAN-only access; no cloud or outside-network exposure | Network | [Q8] |

## Organizational Constraints

| ID | Constraint | Scope | Source |
|----|------------|-------|--------|
| OC-01 | Single user, no reporting or collaborators | Project | [Q2] |
| OC-02 | No hard budget or timeline constraints | Project | [Q6] |

## Regulatory / Compliance Constraints

| ID | Constraint | Scope | Source |
|----|------------|-------|--------|
| RC-01 | None — personal project, home LAN, no compliance obligations | Project | [Q7] |

## Out of Scope

| ID | Item | Reason | Source |
|----|------|--------|--------|
| OS-01 | Autonomous navigation or obstacle avoidance | MVP boundary | [Q8] |
| OS-02 | Multi-robot support | MVP boundary | [Q8] |
| OS-03 | Cloud hosting or outside-LAN access | MVP boundary | [Q8] |

## Assumptions

None.
