# Dependencies — sphero

Versions and manifests are in `technology-stack.md`; component ownership in `component-inventory.md`.

## External Dependencies

- **Python runtime (declared)**: `bleak`, `fastapi` (`pyproject.toml:6-9`, `requirements.txt:1-3`); chat stack `deepagents`, `langchain-openai`, `openai` (`requirements.txt:5-8`) imported lazily in `backend/app/agent_command.py:75-93`.
- **Python runtime (undeclared)**: `uvicorn` is imported/launched by `backend/app` entrypoints, `backend.sh:20` and `u2_telemetry/__main__.py:39` but is not in either manifest.
- **Python test**: `pytest`, `pytest-asyncio`, `coverage` (`requirements.txt:10-13`).
- **Frontend**: `react`, `react-dom` (dependencies); Vite, TypeScript, Tailwind/PostCSS, Vitest, Testing Library, jsdom, coverage-v8 (devDependencies) per `package.json:15-33`.
- **System**: BlueZ + a Bluetooth controller for any real robot path; npm/Node and `python3` for the run scripts; `uv` only for README hardware checks.

## Internal Dependency Edges

| From | To | Nature |
|---|---|---|
| `backend/app/main.py` | `agent_command`, `chat_input`, `config`, `models`, `robot_command` | pipeline construction + WS handling |
| `chat_input.py` | `models`, `config`; injected `AgentTranslator` | validation → translation |
| `agent_command.py` | `models`, `config`; injected `ModelClient` | LLM translation, active speed state |
| `robot_command.py` | `models`, `config`; injected `BleClient` | encode + BLE write + Contract 1 report |
| `u2_telemetry/service.py` | listener, normalizer, publisher, connection/callback handlers | telemetry orchestration |
| `u2_telemetry/__main__.py` | `service`, `event_bus`, `api` | injects the single shared bus into both service publisher and WS endpoint |
| `frontend/src/App.tsx` | `ChatWindow`, `StatsPanel`, `services/api` | one shared command handler |
| `frontend/src/components/StatsPanel.tsx` | `useRobotStateConnection` + 5 presentational components | telemetry container |
| `vite.config.ts` (dev) | U1 `:8000`, U2 `:8001` | WebSocket proxies |

## Cross-Unit / Runtime Coupling

- **Contract 1**: U1 `RobotCommandSender._report_status` → optional sync callback → U2 `handle_command_status`; default no-op in live U1 (`backend/app/main.py:38`).
- **Contract 2**: U2 publisher → one `RobotStateEventBus` → `/ws/robot-state` → U3 hook. Injecting the same bus instance is load-bearing; separate instances would break delivery (`u2_telemetry/__main__.py:63-77`).
- **Build coupling**: Vite emits `dist/`, which U1 serves (`vite.config.ts:18-21`, `backend/app/main.py:100-111`).
- **Known conflict**: BLE identifiers differ across U1 defaults, U2's notification characteristic and the README's recorded vendor service — see `architecture.md` (Improvement Opportunities) and `code-quality-assessment.md`.
