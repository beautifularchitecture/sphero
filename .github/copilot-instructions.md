# Copilot Instructions

## Project architecture

This is a greenfield Sphero Mini control project. The intended app is a React +
TypeScript SPA built with Vite and served by a Python 3.11 FastAPI backend on a
Linux host. The browser sends chat and receives robot telemetry over a
WebSocket. On the backend, chat input is validated, LangChain Deep Agents with
an OpenRouter model translates it into an allowed robot command, and Bluetooth
LE commands are sent to the Sphero Mini through BlueZ and `bleak`. Telemetry
updates flow back to the SPA's stats panel.

The design is split into `ChatInput`, `AgentCommand`, and `RobotCommand` for
chat-to-motion, `RobotTelemetry` for robot state, and `StatsDisplay` for the
UI. Keep commands constrained to the designed vocabulary (movement, stop,
speed, and color); on unclear input or backend/Bluetooth failure, stop the
robot and show the error to the user.

The design record is under
`aidlc/spaces/default/intents/261110-sphero-chat-control/`. Consult its
`inception/domain-design/components.md`,
`construction/u1-chat-command-core/nfr-requirements/tech-stack-decisions.md`,
and `construction/u1-chat-command-core/functional-design/functional-spec.md`
before changing boundaries or behavior. These are design decisions; verify
what has actually been implemented before assuming an app component exists.

## Build, test, and lint

The recorded verification command is `pytest`. The design specifies pytest and
coverage.py for backend tests; run an individual test with
`pytest path/to/test_file.py::test_function`. Once the planned test layout is
present, the documented backend command is:

```bash
pytest tests/ --cov=backend/app --cov-report=term-missing
```

The intended frontend test stack is Vitest with React Testing Library. The
design also names `black --check .`, `ruff check .`, and `mypy .` for backend
quality checks. At the time these instructions were added, application source,
test files, package manifests, and lint configuration were not present; check
the current project files for runnable scripts rather than assuming these
planned commands are configured.

## Repository conventions

- Follow the root `AGENTS.md` for the AI-DLC workflow. Application code belongs
  at the workspace root; AI-DLC records belong under
  `aidlc/spaces/default/intents/<record>/`. Do not hand-edit stage `memory.md`
  observation diaries.
- Use the team's BDD ordering: write Given/When/Then behavior scenarios before
  implementation. The project target is at least 80% line coverage, with tests
  required before merge. Build and verify the chat-to-robot-to-stats walking
  skeleton before adding broader features.
- Keep OpenRouter credentials in the project-root `.env`; never commit `.env`
  or `.env.*`. The app is intended for local/LAN use, but OpenRouter calls
  require outbound internet access.
