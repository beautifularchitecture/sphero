# Code Generation Plan — u1-chat-command-core

Grounded in functional design [functional-spec], rules [rules], entity model [entities.md], user stories [stories], requirements [requirements], contract design [contract-summary], and NFR design [nfr-design/performance-design.md, nfr-design/security-design.md, nfr-design/scalability-design.md, nfr-design/reliability-design.md, nfr-design/observability-design.md].

## Plan Overview

This unit builds the chat command core: chat input handling, AI agent command translation via Deep Agents + OpenRouter, and Bluetooth LE robot command execution. Three components are built in this unit:

- **U1-ChatInput**: Chat message input, validation, and forwarding
- **U1-AgentCommand**: AI agent command translation via Deep Agents + OpenRouter  
- **U1-RobotCommand**: Bluetooth LE command sending to Sphero Mini

Total stories: US1.1 (Chat-driven robot movement), US1.2 (Speed control), US1.3 (LED color control)

## Implementation Steps

| Step | Component | Stories | Acceptance Criteria | Test File(s) |
|------|-----------|---------|-----------------|--------------|
| 1 | ChatInput | US1.1 AC1.1.1-AC1.1.5 | `tests/chat_input/test_chat_input.py` |
| 2 | AgentCommand | US1.1 AC1.1.1-AC1.1.5 | `tests/agent_command/test_agent_command.py` |
| 3 | RobotCommand | US1.1 AC1.1.1-AC1.1.5 | `tests/robot_command/test_robot_command.py` |
| 4 | ChatInput | US1.2 AC1.2.1-AC1.2.3 | `tests/chat_input/test_chat_input_speed.py` |
| 5 | AgentCommand | US1.2 AC1.2.1-AC1.2.3 | `tests/agent_command/test_agent_command_speed.py` |
| 6 | RobotCommand | US1.2 AC1.2.1-AC1.2.3 | `tests/robot_command/test_robot_command_speed.py` |
| 7 | ChatInput | US1.3 AC1.3.1-AC1.3.3 | `tests/chat_input/test_chat_input_color.py` |
| 8 | AgentCommand | US1.3 AC1.3.1-AC1.3.3 | `tests/agent_command/test_agent_command_color.py` |
| 9 | RobotCommand | US1.3 AC1.3.1-AC1.3.3 | `tests/robot_command/test_robot_command_color.py` |

### Step Execution Order

1. **ChatInput** — input validation, message forwarding (US1.1 AC1.1.1-AC1.1.5)
2. **AgentCommand** — AI translation via Deep Agents + OpenRouter (US1.1 AC1.1.1-AC1.1.5)
3. **RobotCommand** — Bluetooth LE command execution (US1.1 AC1.1.1-AC1.1.5)
4. **ChatInput** — speed command validation (US1.2 AC1.2.1-AC1.2.3)
5. **AgentCommand** — speed command translation (US1.2 AC1.2.1-AC1.2.3)
6. **RobotCommand** — speed command Bluetooth execution (US1.2 AC1.2.1-AC1.2.3)
7. **ChatInput** — color command validation (US1.3 AC1.3.1-AC1.3.3)
8. **AgentCommand** — color command translation (US1.3 AC1.3.1-AC1.3.3)
9. **RobotCommand** — color command Bluetooth execution (US1.3 AC1.3.1-AC1.3.3)

### Test Coverage

Test coverage follows the mvp scope floor of 80% line coverage. All requirement-driven acceptance criteria have corresponding test files. Error path tests (unclear input, Bluetooth errors, etc.) are included per the Testing Contract's error-path coverage requirement.

## Files to Create

### Backend (Python + FastAPI + websockets)

| File | Purpose | Stories |
|------|---------|---------|
| `backend/app/main.py` | FastAPI app entry, websocket endpoint | US1.1, US1.2, US1.3 |
| `backend/app/chat_input.py` | Chat input validation and forwarding | US1.1, US1.2, US1.3 |
| `backend/app/agent_command.py` | LangChain Deep Agents + OpenRouter translation | US1.1, US1.2, US1.3 |
| `backend/app/robot_command.py` | Bluetooth LE command sending via bleak | US1.1, US1.2, US1.3 |
| `backend/app/config.py` | Configuration loading from .env | All |
| `backend/app/models.py` | Pydantic models for chat messages and robot commands | US1.1, US1.2, US1.3 |

### Frontend (React + TypeScript)

| File | Purpose | Stories |
|------|---------|---------|
| `frontend/src/App.tsx` | Main app component, chat window + stats panel | US1.1, US1.2, US1.3 |
| `frontend/src/components/ChatWindow.tsx` | Chat input and message list | US1.1, US1.2, US1.3 |
| `frontend/src/components/StatsPanel.tsx` | Stats display (direction, orientation, color, position) | US1.1, US1.2, US1.3 |
| `frontend/src/components/ConnectionStatus.tsx` | Robot connection status indicator | US1.1, US1.2, US1.3 |
| `frontend/src/services/api.ts` | WebSocket client for chat and telemetry | US1.1, US1.2, US1.3 |

### Tests

| File | Purpose | Stories |
|------|---------|---------|
| `tests/chat_input/test_chat_input.py` | Chat input validation tests | US1.1, US1.2, US1.3 |
| `tests/agent_command/test_agent_command.py` | Agent command translation tests | US1.1, US1.2, US1.3 |
| `tests/robot_command/test_robot_command.py` | Robot command Bluetooth execution tests | US1.1, US1.2, US1.3 |
| `tests/conftest.py` | Pytest configuration and fixtures | All |

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before testing robot command execution
- OpenRouter API key must be configured in `.env` before testing agent translation
- Frontend and backend run on the same machine (localhost)
- Bluetooth LE adapter must be available on the Linux host