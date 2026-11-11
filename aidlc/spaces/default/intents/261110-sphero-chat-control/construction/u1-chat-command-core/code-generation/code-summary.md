# Code Summary — u1-chat-command-core

Grounded in functional design [functional-spec], rules [rules], entities [entities.md], user stories [stories], requirements [requirements], contract design [contract-summary], and NFR design [nfr-design].

## Files Generated

| File | Purpose | Stories |
|------|---------|---------|
| `backend/app/main.py` | FastAPI app entry, websocket endpoint for chat input | US1.1, US1.2, US1.3 |
| `backend/app/chat_input.py` | Chat input validation and forwarding to AgentCommand | US1.1, US1.2, US1.3 |
| `backend/app/agent_command.py` | LangChain Deep Agents + OpenRouter translation | US1.1, US1.2, US1.3 |
| `backend/app/robot_command.py` | Bluetooth LE command sending to Sphero Mini | US1.1, US1.2, US1.3 |
| `backend/app/config.py` | Configuration loading from .env | All |
| `backend/app/models.py` | Pydantic models for chat messages and robot commands | US1.1, US1.2, US1.3 |
| `frontend/src/App.tsx` | Main app component, chat window + stats panel | US1.1, US1.2, US1.3 |
| `frontend/src/components/ChatWindow.tsx` | Chat input and message list | US1.1, US1.2, US1.3 |
| `frontend/src/components/StatsPanel.tsx` | Stats display (direction, orientation, color, position) | US1.1, US1.2, US1.3 |
| `frontend/src/components/ConnectionStatus.tsx` | Robot connection status indicator | US1.1, US1.2, US1.3 |
| `frontend/src/services/api.ts` | WebSocket client for chat input and telemetry | US1.1, US1.2, US1.3 |

## Tests Written

| File | Tests | Stories |
|------|-------|---------|
| `tests/chat_input/test_chat_input.py` | Chat input validation: valid, empty, whitespace, invalid UTF-8, command parsing | US1.1, US1.2, US1.3 |
| `tests/agent_command/test_agent_command.py` | Agent translation: free-form to commands, vocabulary validation | US1.1, US1.2, US1.3 |
| `tests/robot_command/test_robot_command.py` | Robot command: Bluetooth LE sending, speed, color | US1.1, US1.2, US1.3 |

## Decisions

- Used FastAPI for backend with websockets for real-time chat
- Used React for frontend SPA with websocket client
- Used LangChain Deep Agents with OpenRouter for chat-to-command translation
- Used bleak for Bluetooth LE communication with Sphero Mini
- Single-user model: no authentication required for chat input
- Robot commands: forward, back, left, right, stop, setSpeed, setColor

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before testing robot command execution
- OpenRouter API key must be configured in .env before testing agent translation
- Backend and frontend run on the same machine (localhost)
- Bluetooth LE adapter must be available on the Linux host
- No multi-user support (single-user desktop application)
- No cloud hosting (LAN-only per NFR1)