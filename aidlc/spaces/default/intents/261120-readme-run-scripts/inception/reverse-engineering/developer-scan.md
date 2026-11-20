## Developer Code Scan Results

### Scan Coverage

- **Analyzed deeply**:
  - `README.md`, `.gitignore`, `backend.sh`, `frontend.sh`, `opencode.json`
  - Root build/config/docs: `package.json`, `package-lock.json` (declared versions only), `pyproject.toml`, `requirements.txt`, `vite.config.ts`, `vitest.config.ts`, `tsconfig.json`, `tailwind.config.js`, `postcss.config.js`, `u2-telemetry.service`, `DEPLOYMENT-u2-telemetry.md`, `RESPONSE.md`
  - `backend/app/` — all 7 Python modules (`__init__.py`, `main.py`, `config.py`, `models.py`, `chat_input.py`, `agent_command.py`, `robot_command.py`)
  - `u2_telemetry/` — all 11 production Python modules (`__init__.py`, `__main__.py`, `models.py`, `normalizer.py`, `event_bus.py`, `event_publisher.py`, `ble_listener.py`, `connection_handler.py`, `callback_handler.py`, `api.py`, `service.py`)
  - `frontend/` — `index.html` and all production sources under `src/` (`main.tsx`, `App.tsx`, `types.ts`, `constants.ts`, `index.css`, `services/api.ts`, `hooks/useRobotStateConnection.ts`, `test-setup.ts`, `test-utils/mockWebSocket.ts`, and all 7 components)
  - `.github/workflows/ci.yml`, `.github/copilot-instructions.md`
- **Skimmed only**:
  - `tests/` — all seven test folders enumerated; `tests/integration/test_walking_skeleton.py` and `tests/main/test_main.py` read in full, other layer suites classified by filename and purpose
  - `u2_telemetry/tests/` — all ten test modules enumerated; `test_service.py` read in full, others classified by filename and purpose
  - `frontend/src/**/*.test.{ts,tsx}` — all 13 test modules enumerated; `integration-websocket-to-ui.test.tsx` and `components/StatsPanel.test.tsx` read in full, others classified by filename and purpose
  - `package-lock.json` — dependency versions taken from `package.json`; lock body not opened
- **Left out** (per "What to Skip"; no files inside them opened or named in the synthesized artifacts):
  - harness/install and workspace directories (`.aidlc/`, `.opencode/`, `aidlc/`) and git metadata (`.git/`)
  - build outputs (`dist/`, `coverage/`)
  - dependency folder (`node_modules/`)
  - tool/Python caches (`.pytest_cache/`, `__pycache__/`, `.coverage`)

### Packages Found

- U1 chat-command core (`backend/app/`) — application package — Python — WebSocket chat → LLM translation → BLE command; FastAPI entrypoint.
- U2 RobotTelemetry (`u2_telemetry/`) — application package — Python — BLE telemetry receive → normalize → publish `robot.state.changed`.
- U3 stats UI SPA (`frontend/`) — application package — TypeScript/React — chat window plus robot-state stats panel over two WebSockets.
- U1/U2 test suite (`tests/`, `u2_telemetry/tests/`) — tests — Python — BDD pytest scenarios with injected offline doubles.
- U3 test suite (co-located under `frontend/src/`) — tests — TypeScript — Vitest + React Testing Library, jsdom.
- Run scripts (`backend.sh`, `frontend.sh`) — scripts — Bash — start backends and SPA dev server.
- CI workflow (`.github/workflows/ci.yml`) — pipeline — YAML — GitHub Actions gates for both languages.

### Build System

- **Type**: polyglot — Vite/npm for the SPA, pip/pyproject for Python services, no single monorepo build orchestrator.
- **Config Files**: `package.json`, `package-lock.json`, `vite.config.ts`, `vitest.config.ts`, `tsconfig.json`, `tailwind.config.js`, `postcss.config.js`, `pyproject.toml`, `requirements.txt`, `.github/workflows/ci.yml`.
- **Build Dependencies**: Vite `root: 'frontend'` emits to root `dist/`, which U1's FastAPI app serves as static files; `frontend.sh` installs npm deps on first run; CI runs `npm ci`, `npm run typecheck`, `vitest`, `npm run build`, then pip-installs `requirements.txt` for the Python jobs.

### APIs Discovered

- HTTP `GET /health` — `backend/app/main.py:215` — liveness, no dependency checks.
- HTTP `GET /` and mounted `/assets` — `backend/app/main.py:223-229` — serve built SPA or a helpful 404.
- WebSocket `/ws/chat` — `backend/app/main.py:219` — 1 request frame, 1 response frame (ack or typed error); 2 entry paths, 5 error branches.
- WebSocket `/ws/robot-state` — `u2_telemetry/api.py:49` — subscribes clients to the shared in-process bus; broadcasts 1 topic.
- Contract 1 sync callback — `u2_telemetry/service.py:86` — `CommandExecutionStatus {commandId, status, timestamp}` injected U1 → U2; U1 default is a documented no-op (`backend/app/main.py:38`).
- BLE GATT boundary — `backend/app/robot_command.py:99`, `u2_telemetry/ble_listener.py:96` — one control write characteristic, one telemetry notification characteristic.
- No authentication on any HTTP/WebSocket surface; LAN-only use is declared in `frontend/src/constants.ts:15`.

### Frameworks & Libraries

See `technology-stack.md` in the staged candidate for versions; source of truth is `package.json`, `pyproject.toml`, `requirements.txt`. Highlights: FastAPI + Pydantic + bleak + uvicorn (Python), LangChain-OpenAI / Deep Agents / OpenAI (lazy, chat translation), React 18 + Vite 5 + Tailwind 3 + Vitest 1 + Testing Library (frontend), pytest / pytest-asyncio + coverage.py (Python tests).

### Test Coverage

- **Test Directories**: `tests/` (7 areas: agent_command, chat_input, config, integration, main, models, robot_command), `u2_telemetry/tests/`, co-located `frontend/src/**/*.test.{ts,tsx}` (7 component, 2 integration, 1 hook, 1 service).
- **Test Frameworks**: pytest + pytest-asyncio with `asyncio_mode = "auto"` (Python); Vitest + jsdom + @testing-library/react + jest-dom (frontend).
- **Coverage Config**: present — `[tool.coverage.run]` / `[tool.coverage.report] fail_under = 80` in `pyproject.toml`; CI enforces 80% line floors for U1 (`tests/`), U2 (`u2_telemetry/`) and the SPA (`vitest --coverage --coverage.thresholds.lines=80`).

### Code Quality Indicators

- **Linting**: no lint/format config or CI lint step found; design docs name `black`, `ruff`, `mypy` as planned only. One `eslint-disable-next-line react-hooks/exhaustive-deps` in `frontend/src/hooks/useRobotStateConnection.ts:263` with no ESLint config present.
- **CI/CD**: `.github/workflows/ci.yml` — frontend job (typecheck, tests+coverage, build, bundle secret scan, artifact upload), backend job (U1+U2 pytest with 80% floors), `ci-ok` aggregate; triggers on push and PR to `main`.
- **Documentation**: README covers hardware/BLE checks and `pytest` verification but not app startup; `DEPLOYMENT-u2-telemetry.md` documents U2 install/service/config; `.github/copilot-instructions.md` describes architecture and conventions; production modules carry detailed docstrings.

### Technical Debt Signals

- Stale README status claim: `README.md:8-14` says the app "is still being designed" and that the checks do not test the web app/WebSocket/agent/UI, though all three units now exist and have run scripts and CI.
- `uvicorn` is imported and launched (`backend/app/...`, `backend.sh:20`, `u2_telemetry/__main__.py:39`) but is not declared in `requirements.txt`; only `fastapi` is.
- BLE UUIDs disagree across units: U1 control defaults `6e400001-…/6e400002-…` (`backend/app/config.py:25-26`) vs the Sphero vendor service recorded in `README.md:164` and U2's telemetry characteristic `0000ffe1-…` (`u2_telemetry/ble_listener.py:18`).
- Bare `pytest` recorded in `README.md:206-216` conflicts with `pyproject.toml:15` `testpaths = ["u2_telemetry/tests"]` and the two explicit unit-scoped CI commands.
- Broad `except Exception` suppressions at BLE/publisher boundaries carry `# noqa: BLE001` justifications (9 occurrences); no TODO/FIXME/HACK markers found.
- `RESPONSE.md` is a stale advisory review note (NOT-READY) recording unresolved cross-unit contract/business-rule contradictions from an earlier design iteration.

## Handoff Summary

- **Intent-relevant finding**: The README has no "how to run the app" section. It still says at `README.md:8-10` that "The application is still being designed" and that the hardware checks "do not test the planned web app, WebSocket, AI agent, or telemetry UI", and its only verification guidance (`README.md:204-220`) is `pytest` plus BLE smoke scripts. The runnable app is already present and documented elsewhere in the repo: `backend.sh:1-46` starts U1 on `:8000` and optionally U2 on `:8001` when `U2_BLE_ADDRESS` is set; `frontend.sh:1-19` installs npm deps if needed and starts the SPA on `:5173`, with Vite proxies `/ws/chat → 8000` and `/ws/robot-state → 8001` (`vite.config.ts:12-16`); `backend/app/config.py:126-131` fails fast unless `OPENROUTER_API_KEY` is in the environment or project-root `.env`; `u2_telemetry/__main__.py:5-10` documents `U2_BLE_ADDRESS` and `U2_WS_PORT`. These are the concrete facts a README "how to use this" section must convey.
- **Risks / follow-up**: (1) Do not repeat the stale "still being designed" claim — it contradicts implemented code. (2) Any new run instructions must keep the OpenRouter key in `.env` (gitignored) and must not claim the LAN WebSockets are authenticated. (3) If the README is updated with test commands, use the two CI commands rather than the bare `pytest` line. (4) `uvicorn` is an undeclared runtime dependency; mention it or fix the manifest in a separate change, not silently in README prose. (5) No files or folders outside the pre-scan snapshot path `./` were analyzed.
