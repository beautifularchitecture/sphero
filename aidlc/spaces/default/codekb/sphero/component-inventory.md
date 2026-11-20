# Component Inventory — sphero

Six components; file lists are in `code-structure.md` and edges in `dependencies.md`.

### U1 Chat Command Core

- **Location**: `backend/app/`
- **Responsibility**: FastAPI entrypoint, `/health`, `/ws/chat`, static SPA serving; chat validation, LLM translation with one retry and active-speed state, BLE command send with one retry/reconnect, Contract 1 status callback injection.
- **Key types**: `ChatPipeline`, `ChatInput`, `AgentCommand`, `DeepAgentsModelClient`, `RobotCommandSender`, `BleakBleClient`, `Settings`, Pydantic domain models.
- **Depends on**: `bleak` (lazy), `langchain-openai` (lazy), `deepagents` (optional lazy), FastAPI/Pydantic, `OPENROUTER_API_KEY`, built `dist/`.

### U2 RobotTelemetry Service

- **Location**: `u2_telemetry/`
- **Responsibility**: BLE notification reception and reconnect loop, lenient `RobotState` normalization, fire-and-forget publish on `robot.state.changed`, Contract 1 status recording, `/ws/robot-state` delivery through one shared bus.
- **Key types**: `RobotTelemetryService`, `BLEListener`, `RobotStateNormalizer`, `EventPublisher`, `RobotStateEventBus`, `ConnectionHandler`, `CommandStatusCallbackHandler`, `RobotState`.
- **Depends on**: `bleak`, optional FastAPI/uvicorn transport, `U2_BLE_ADDRESS`, `U2_WS_PORT`.

### U3 Stats UI SPA

- **Location**: `frontend/` (`index.html`, `src/`)
- **Responsibility**: chat window, stats panel composed of LAN-risk banner, connection status, robot-state fields, event counter/stale markers, speed/color buttons and error display; one-shot chat WebSocket transport and a resilient telemetry subscription with exponential reconnect.
- **Key types**: `App`, `ChatWindow`, `StatsPanel`, `ConnectionStatus`, `RobotStateDisplay`, `SpeedColorSelector`, `LanRiskBanner`, `ErrorDisplay`, `sendChatCommand`, `useRobotStateConnection`.
- **Depends on**: React 18, Vite dev proxies to ports 8000/8001; no direct BLE or LLM access.

### Run Scripts

- **Location**: `backend.sh`, `frontend.sh`
- **Responsibility**: operator entrypoints. `backend.sh` checks `python3`, warns on missing `.env`, starts U1 on `:8000`, starts U2 on `:8001` only when `U2_BLE_ADDRESS` is set, and traps cleanup. `frontend.sh` checks `npm`, runs `npm install` when `node_modules/` is absent, then `npm run dev` on `:5173`.
- **Depends on**: Python 3 + uvicorn (U1/U2), npm/Node, optional `OPENROUTER_API_KEY` in `.env`.

### CI Pipeline

- **Location**: `.github/workflows/ci.yml`
- **Responsibility**: push/PR gates on `main` — frontend typecheck, Vitest with 80% line floor, production build, bundle secret scan, artifact upload; backend pytest for U1 and U2 with 80% floors; aggregate `ci-ok`.
- **Depends on**: GitHub Actions, Node 20, Python 3.14, `package.json` scripts, `requirements.txt`.

### Project Documentation & Configuration

- **Location**: `README.md`, `DEPLOYMENT-u2-telemetry.md`, `RESPONSE.md`, `.github/copilot-instructions.md`, root build/config manifests (`pyproject.toml`, `requirements.txt`, `package.json`, `vite.config.ts`, `vitest.config.ts`, `tsconfig.json`, `tailwind.config.js`, `postcss.config.js`, `u2-telemetry.service`, `.gitignore`).
- **Responsibility**: operator-facing hardware checks and verification guidance, U2 deployment/service instructions, architecture/convention guidance for contributors, and toolchain configuration. The README is the artifact this intent will change; it currently lacks app run instructions.
