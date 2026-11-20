# Code Structure — sphero

## Package / Module Organization

| Area | Root | Contents |
|---|---|---|
| U1 chat core | `backend/app/` | `main.py` (FastAPI + WS handler), `chat_input.py`, `agent_command.py`, `robot_command.py`, `models.py`, `config.py`, `__init__.py` |
| U1 tests | `tests/` | Seven areas: `main/`, `chat_input/`, `agent_command/`, `robot_command/`, `models/`, `config/`, `integration/` |
| U2 telemetry | `u2_telemetry/` | `service.py`, `ble_listener.py`, `normalizer.py`, `event_publisher.py`, `event_bus.py`, `connection_handler.py`, `callback_handler.py`, `api.py`, `models.py`, `__main__.py`, `__init__.py` |
| U2 tests | `u2_telemetry/tests/` | Ten `test_*.py` modules mirroring the production modules |
| U3 SPA | `frontend/src/` | `main.tsx`, `App.tsx`, `types.ts`, `constants.ts`, `index.css`, `services/`, `hooks/`, `components/` |
| Run/build | repo root | `backend.sh`, `frontend.sh`, Vite/Vitest/TS/Tailwind/PostCSS configs, `package.json`, `pyproject.toml`, `requirements.txt` |

## File Classification

- **Controller/Handler**: `backend/app/main.py` (HTTP + WS), `u2_telemetry/api.py` (WS), `frontend/src/App.tsx` (composition root).
- **Service/UseCase**: `chat_input.py`, `agent_command.py`, `robot_command.py`, `u2_telemetry/service.py`.
- **Model/Entity**: `backend/app/models.py` (Pydantic), `u2_telemetry/models.py` (dataclass), `frontend/src/types.ts`.
- **Repository/DAO (boundary adapters)**: `BleakBleClient`, `BLEListener`, `DeepAgentsModelClient`, `frontend/src/services/api.ts`.
- **Utility/Helper**: `backend/app/config.py` (settings + structured logging), `u2_telemetry/normalizer.py`, `frontend/src/constants.ts`, `test-utils/mockWebSocket.ts`.
- **Middleware/infrastructure**: `u2_telemetry/event_bus.py`, `event_publisher.py`, `connection_handler.py`, `callback_handler.py`, `frontend/src/hooks/useRobotStateConnection.ts`.
- **Static/Asset**: `frontend/index.html`, `frontend/src/index.css`.
- **Configuration**: root config manifests, `.github/workflows/ci.yml`, `u2-telemetry.service`.
- **Test**: all files under the three test areas above plus co-located `frontend/src/**/*.test.*`.

## Code Patterns

- Dependency inversion via `Protocol` types and constructor injection; production adapters are defaults, tests inject doubles.
- Dataclass/Pydantic value objects; all enums derive from `str` for JSON-friendly serialization.
- Structured JSON logging in U1 with secret redaction (`Settings.for_logging`); plain logging in U2.
- BDD test names (`test_given_..._when_..._then_...`) with inline Given/When/Then comments, mirrored in Vitest `it('Given ... When ... Then ...')`.
- Stable `data-testid` attributes on all interactive/tested UI elements.

Full inventory and dependency edges are in `component-inventory.md` and `dependencies.md`; API contracts in `api-documentation.md`.
