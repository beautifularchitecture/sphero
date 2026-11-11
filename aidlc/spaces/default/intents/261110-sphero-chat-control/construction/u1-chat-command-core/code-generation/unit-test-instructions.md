# Unit Test Instructions — u1-chat-command-core

## Test Framework Setup

This unit uses pytest for Python backend testing and Vitest + React Testing Library for frontend SPA testing, per the affirmed test posture (BDD methodology, 80% line coverage floor, CI before merge).

## Test Runner Command

Run all unit tests for this unit:

```bash
cd /home/supermind/Code/the-beautiful-architecture/sphero
pytest tests/ --cov=backend/app --cov-report=term-missing
```

## Test File Structure

```
tests/
├── chat_input/
│   ├── __init__.py
│   └── test_chat_input.py
├── agent_command/
│   ├── __init__.py
│   └── test_agent_command.py
└── robot_command/
    ├── __init__.py
    └── test_robot_command.py
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
# Run all unit tests for this unit
cd /home/supermind/Code/the-beautiful-architecture/sphero
pytest tests/ --cov=backend/app --cov-report=term-missing

# Run only chat input tests
pytest tests/chat_input/ --cov=backend/app --cov-report=term-missing

# Run only agent command tests
pytest tests/agent_command/ --cov=backend/app --cov-report=term-missing

# Run only robot command tests
pytest tests/robot_command/ --cov=backend/app --cov-report=term-missing
```

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before testing robot command execution
- OpenRouter API key must be configured in `.env` before testing agent command translation
- Frontend (React SPA) testing is not part of this unit (U3 handles frontend)