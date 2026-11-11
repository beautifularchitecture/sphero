# Code Summary — u1-chat-command-core

Grounded in functional design [functional-spec], requirements [requirements], unit-of-work [unit-of-work], contract design [contract-summary], and NFR design [nfr-design].

## Files Created

| File | Purpose | Stories |
|------|---------|---------|
| backend/app/main.py | FastAPI app entry, websocket server for chat input | US1.1, US1.2, US1.3 |
| backend/app/chat_input.py | Chat input validation and forwarding to AgentCommand | US1.1, US1.2, US1.3 |
| backend/app/agent_command.py | LangChain Deep Agents + OpenRouter chat-to-command translation | US1.1, US1.2, US1.3 |
| backend/app/robot_command.py | Bluetooth LE command sending to Sphero Mini | US1.1, US1.2, US1.3 |
| backend/app/config.py | Configuration loading from .env | All |
| backend/app/models.py | Pydantic models for chat messages and robot commands | US1.1, US1.2, US1.3 |
| frontend/src/App.tsx | Main app component, chat window + stats panel | US1.1, US1.2, US1.3 |
| frontend/src/components/ChatWindow.tsx | Chat input and message list | US1.1, US1.2, US1.3 |
| frontend/src/components/StatsPanel.tsx | Stats panel (direction, orientation, color, position) | US1.1, US1.2, US1.3 |
| frontend/src/components/ConnectionStatus.tsx | Robot connection status indicator | US1.1, US1.2, US1.3 |
| frontend/src/services/api.ts | WebSocket client for chat input and telemetry | US1.1, US1.2, US1.3 |

## Tests Written

| File | Tests | Stories |
|------|-------|---------|
| tests/chat_input/test_chat_input.py | Chat input validation (valid, empty, whitespace, invalid UTF-8, command parsing) | US1.1, US1.2, US1.3 |
| tests/agent_command/test_agent_command.py | Agent translation (free-form chat to robot commands, validation against allowed vocabulary) | US1.1, US1.2, US1.3 |
| tests/robot_command/test_robot_command.py | Robot command execution (Bluetooth LE commands, speed, color) | US1.1, US1.2, US1.3 |

## Decisions

- **Backend**: FastAPI with websockets for real-time chat input and telemetry streaming
- **Frontend**: React SPA served by FastAPI backend
- **AI Agent**: LangChain Deep Agents + OpenRouter for chat-to-command translation
- **Bluetooth LE**: bleak/pygatt library for Sphero Mini communication
- **Testing**: pytest + coverage.py for Python backend; Vitest + React Testing Library for frontend SPA

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before testing robot command execution
- OpenRouter API key must be configured in `.env` before testing agent command translation
- Frontend and backend run on the same machine (localhost)
- Bluetooth LE adapter must be available on the Linux host
- No multi-user support (single-user desktop application)
- No cloud hosting (LAN-only per NFR1)