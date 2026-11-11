# Feasibility Assessment — Sphero Mini Chat Control

## Technical Viability

Grounded in the intent statement captured in intent-capture [intent-statement]. The initiative is feasible on a single Linux machine with local Bluetooth. A Python backend using FastAPI and websockets can expose a local website, and LangChain Deep Agents with an OpenRouter model can translate free-form chat into robot commands. The Sphero Mini (original) connects via BlueZ and a Python Bluetooth LE library such as bleak or pygatt, paired once at setup. [Q1] [Q6] [desc] [scope]

## Backend Architecture

The backend runs on Linux and exposes two websocket surfaces: one for chat input from the SPA, and one for robot telemetry output to the SPA stats panel. Chat messages flow to LangChain Deep Agents backed by an OpenRouter model, which emits robot instructions (movement direction, speed, heading/orientation, LED color). A Bluetooth LE adapter drives the Sphero Mini directly. [Q2] [Q3] [Q4] [Q6]

## Frontend Architecture

The SPA is a React frontend served by the FastAPI backend. It contains a chat window for user input and a stats panel showing direction, orientation, color, and position, refreshed on every robot state change over the telemetry websocket. [Q2] [Q5]

## Robot Commands in Scope

Directional movement (forward, back, left, right, stop), speed control, heading/orientation, and LED color. No autonomous navigation or obstacle avoidance, no multi-robot support, and no cloud or outside-LAN access. [Q3] [Q8]

## Failure Behaviour

When the agent is uncertain or something fails, the robot stops and the error is shown in the UI. [Q5]

## OpenRouter Model Integration

LangChain Deep Agents package is used directly, with the OpenRouter model behind it. The API key is loaded from a `.env` file at project root at backend startup and is never committed. [Q3] [Q4]

## Constraints and Assumptions

- Budget and timeline: no hard constraints — build until it works reliably. [Q6]
- Compliance: none — personal project, home LAN, no compliance obligations. [Q7]
- Success metric: works reliably on the LAN; exact latency is not a critical target for this MVP. [Q7]
- Robot model: Sphero Mini (original). [Q6]

## Verdict

Feasible. No technical blockers identified for an MVP on a single Linux machine with local Bluetooth and LAN-only networking. [Q1] [Q6] [Q7]

## Assumptions & Open Questions

None.
