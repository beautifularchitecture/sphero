# Unit Test Instructions — u1-chat-command-core

## Test Framework Setup

This unit uses pytest for the Python backend and Vitest + React Testing Library for the U1 frontend slice it owns (`ChatWindow`, `services/api.ts`), per the affirmed test posture (BDD methodology, 80% line coverage floor, CI before merge).

## Test Runner Command

Run all backend unit tests for this unit:

```bash
cd /home/supermind/Code/the-beautiful-architecture/sphero
python3 -m pytest tests/ --cov=backend/app --cov-report=term-missing
```

(`python3` because this host has no `python` alias; the command is otherwise the recorded one.)

The U1 frontend tests run under the project Vitest configuration with the rest of the SPA suite:

```bash
npx vitest run frontend/src/components/ChatWindow.test.tsx frontend/src/services/api.test.ts
```

## Test File Structure

```
tests/
├── chat_input/
│   ├── __init__.py
│   └── test_chat_input.py
├── agent_command/
│   ├── __init__.py
│   ├── test_agent_command.py
│   ├── test_agent_command_speed.py
│   └── test_agent_command_color.py
└── robot_command/
    ├── __init__.py
    ├── test_robot_command.py
    ├── test_robot_command_speed.py
    └── test_robot_command_color.py

frontend/src/components/ChatWindow.test.tsx
frontend/src/services/api.test.ts
```

## Acceptance Criteria to Test

### US1.1 — Chat-driven Robot Movement

| AC | Test File | Test Cases |
|----|-----------|------------|
| AC1.1.1 | tests/chat_input/test_chat_input.py | "roll forward" → robot moves forward |
| AC1.1.2 | tests/chat_input/test_chat_input.py | "stop" → robot stops moving |
| AC1.1.3 | tests/chat_input/test_chat_input.py | "turn left" → robot turns left |
| AC1.1.4 | tests/chat_input/test_chat_input.py | "turn right" → robot turns right |
| AC1.1.5 | tests/chat_input/test_chat_input.py | "roll back" → robot moves backward |

### US1.2 — Speed Control

| ID | Test File | Test Cases |
|----|-----------|------------|
| AC1.2.1 | tests/agent_command/test_agent_command_speed.py | "set speed low" → speed=low |
| AC1.2.2 | tests/agent_command/test_agent_command_speed.py | "set speed medium" → speed=medium |
| AC1.2.3 | tests/agent_command/test_agent_command_speed.py | "set speed high" → speed=high |

### US1.3 — LED Color Control

| ID | Test File | Test Cases |
|----|-----------|------------|
| AC1.3.1 | tests/agent_command/test_agent_command_color.py | "set color red" → LED turns red |
| AC1.3.2 | tests/agent_command/test_agent_command_color.py | "set color blue" → LED turns blue |
| AC1.3.3 | tests/agent_command/test_agent_command_color.py | "set color green" → LED turns green |

## Running Tests

```bash
# Run all backend unit tests for this unit
cd /home/supermind/Code/the-beautiful-architecture/sphero
python3 -m pytest tests/ --cov=backend/app --cov-report=term-missing

# Run only chat input tests
python3 -m pytest tests/chat_input/ --cov=backend/app --cov-report=term-missing

# Run only agent command tests
python3 -m pytest tests/agent_command/ --cov=backend/app --cov-report=term-missing

# Run only robot command tests
python3 -m pytest tests/robot_command/ --cov=backend/app --cov-report=term-missing
```

## Endpoint and Error Coverage

- `backend/app/main.py`: `/health` returns 200; the chat WebSocket accepts a
  message and returns the translated command or a plain-language error; static
  serving returns `dist/index.html`.
- `backend/app/chat_input.py`: empty, whitespace-only, invalid UTF-8, unknown
  command and over-long input are rejected with a message.
- `backend/app/agent_command.py`: model failure retries once, then surfaces an
  error; the injected fake client keeps the suite offline.
- `backend/app/robot_command.py`: a failed BLE send retries once with backoff;
  a disconnection triggers reconnect; a failed connection never moves the robot
  and signals the chat error path.
- `backend/app/config.py`: missing `OPENROUTER_API_KEY` fails startup with a
  clear message; the key value is never logged.

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before a live robot run
- OpenRouter API key must be configured in `.env` before a live agent run; the automated suite injects a fake model client and needs no key
- Frontend stats components are U3's and stay out of this unit; U1 tests only `ChatWindow` and `services/api.ts`
- The U1 frontend tests run in jsdom under the project Vitest configuration; no real browser is used