# Unit Test Instructions — u1-chat-command-core

## Test Framework Setup

This unit uses pytest as the test framework with coverage.py for coverage measurement.

### Test Runner Command

Run all unit tests for this unit:

```bash
cd aidlc/spaces/default/intents/261110-sphero-chat-control/construction/u1-chat-command-core
pytest tests/ --cov=. --cov-report=term-missing
```

### Test File Structure

```
tests/
├── __init__.py
├── chat_input/
│   ├── __init__.py
│   └── test_chat_input.py
├── agent_command/
│   ├── __init__.py
│   └── test_agent_command.py
├── robot_command/
│   ├── __init__.py
│   └── test_robot_command.py
└── conftest.py
```

### Test Coverage Requirements

Minimum 80% line coverage per NFR7.1. Coverage is measured across the `backend/app/` source directory.

### Test Categories

#### Happy Path Tests
Each requirement's happy path acceptance criteria must have corresponding tests:
- AC1.1.1: "roll forward" command moves robot forward
- AC1.1.2: "stop" command stops robot
- AC1.1.3: "turn left" command turns robot left
- AC1.1.4: "turn right" command turns robot right
- AC1.1.5: "roll back" command moves robot backward
- AC1.2.1: "set speed low" sets speed to low
- AC1.2.2: "set speed medium" sets speed to medium
- AC1.2.3: "set speed high" sets speed to high
- AC1.3.1: "set color red" sets LED color to red
- AC1.3.2: "set color blue" sets LED color to blue
- AC1.3.3: "set color green" sets LED color to green

#### Error Path Tests (BDD - Given/When/Then)

**Given** an unclear chat message **"xyzzy"**, **When** user sends it via chat, **Then** system asks user to rephrase before any robot action.

**Given** Bluetooth permission is denied, **When** backend tries to connect, **Then** error is shown in chat UI and robot does not move.

**Given** robot disconnects mid-operation, **When** disconnect occurs, **Then** error is shown in chat UI and movement stops.

**Given** agent or backend encounters an error, **When** error occurs, **Then** robot stops and error is shown in chat UI.

### Running Tests

Run all unit tests for this unit:

```bash
cd aidlc/spaces/default/intents/261110-sphero-chat-control/construction/u1-chat-command-core
pytest tests/ --cov=. --cov-report=term-missing
```

### Test Execution Order

1. ChatInput tests (Q1: chat input validation)
2. AgentCommand tests (Q2: agent command translation)
3. RobotCommand tests (Q3: robot command Bluetooth execution)

### Mocking

- Bluetooth LE: Mock the bleak/pygatt library; do not require actual Bluetooth hardware for unit tests
- OpenRouter API: Mock the API responses; do not require actual API key for unit tests
- Frontend: Not tested in this unit (frontend is U3)

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before integration testing robot commands
- OpenRouter API key must be configured for agent command translation tests