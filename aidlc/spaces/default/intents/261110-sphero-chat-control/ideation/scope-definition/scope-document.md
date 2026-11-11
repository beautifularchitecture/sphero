# Scope Document — Sphero Mini Chat Control

Grounded in the intent statement [intent-statement], feasibility assessment [feasibility-assessment], and constraint register [constraint-register].

## In Scope (MVP)

| Capability | Priority | Source |
|------------|----------|--------|
| Chat → robot movement: forward, back, left, right, stop | Must | [Q1] [Q2-A] |
| LED color control | Must | [Q1] [Q2-B] |
| Speed control | Must | [Q2-C] |
| Stats panel: direction, orientation, color, position | Must | [Q1] [Q2-D] |
| Error shown in UI on failure | Must | [Q2-E] |
| Heading/orientation turn-to-direction command | Nice-to-have | [Q2-F] |
| Connection status indicator | Nice-to-have | [Q2-G] |

## Out of Scope (MVP)

| Item | Reason | Source |
|------|--------|--------|
| Autonomous navigation or obstacle avoidance | MVP boundary | [Q8-Intent] [scope-def Q8] |
| Multi-robot support | MVP boundary | [Q8-Intent] [scope-def Q8] |
| Cloud hosting or access from outside the local network | MVP boundary | [Q8-Intent] [scope-def Q8] |

## Tech Stack

| Layer | Choice | Source |
|-------|--------|--------|
| Backend | FastAPI + websockets, Python, Linux | [Q2-Feas] [Q1-Feas] [Q6-Feas] |
| Frontend | React SPA served by the backend | [Q2-Feas] |
| Agent | LangChain Deep Agents package directly | [Q3-Feas] |
| Model | OpenRouter chat model behind Deep Agents | [Q3-Feas] |
| API key | `.env` at project root, never committed | [Q4-Feas] |
| Robot connection | BlueZ + Python Bluetooth LE library (bleak/pygatt) | [Q1-Feas] |
| Pairing | Once at setup | [Q1-Feas] |
| Stats refresh | On every robot state change | [Q5-Feas] |

## Scope Boundary

- **Single user**, no reporting or collaborators [Q2-Intent] [OC-01]
- **LAN only**, no cloud or outside-network access [Q8-Intent] [TC-11]
- **No hard deadlines** — build until it works reliably [Q5] [Q6-Feas]
- **No compliance obligations** — personal project, home LAN [Q7-Feas] [RC-01]
- **Sphero Mini (original)**, backend on Linux [Q6-Intent] [TC-01]

## Assumptions & Open Questions

None.
