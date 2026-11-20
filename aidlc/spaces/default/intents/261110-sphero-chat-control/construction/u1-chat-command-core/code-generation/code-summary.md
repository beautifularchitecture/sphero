# Code Summary — u1-chat-command-core

Grounded in functional design [functional-spec], requirements [requirements], unit-of-work [unit-of-work], contract design [contract-summary], and NFR design [nfr-design].

Loop-back repair attempt 2 produced the complete runnable U1 slice: six backend
modules, the pytest suite, the U1 chat frontend, and the `App.tsx` composition.
U3-owned components were left untouched.

## Files Created / Updated

| File | Purpose | Stories / Requirements |
|------|---------|------------------------|
| backend/app/__init__.py | Package marker | All |
| backend/app/config.py | `.env`/env `Settings`, secret redaction, structured logging | NFR2.1, NFR3.4, NFR9.2 |
| backend/app/models.py | Pydantic models/enums, Contract 1 `CommandExecutionStatus` (camelCase aliases) | BR1.2, BR1.4 |
| backend/app/chat_input.py | UTF-8/non-empty/command-pattern validation and agent forwarding | FR1.1, FR3, BR1.1 |
| backend/app/agent_command.py | Injectable LLM translation, retry/backoff, Deep Agents → direct ChatOpenAI fallback | FR1.1, FR1.2, FR2, BR1.2 |
| backend/app/robot_command.py | Injectable BLE sender, reconnect/retry, Contract 1 status callback | FR1.1, BR1.4, AC1.5.3 |
| backend/app/main.py | FastAPI `/health`, `/ws/chat` ack/error envelopes, SPA serving, pipeline factory | FR4, BR1.3 |
| requirements.txt | Added `deepagents`, `langchain-openai`, `openai`; retained existing pins | All |
| frontend/src/services/api.ts | One-shot chat WebSocket transport with injectable socket factory, ack/error/timeout handling | FR4, BR1.3 |
| frontend/src/components/ChatWindow.tsx | Message list, input form, validation hint, disabled-while-sending state | US1.1, FR4 |
| frontend/src/App.tsx | Composition root: ChatWindow + U3 StatsPanel share `onSendChatCommand`; errors forwarded to `ErrorDisplay` props | US1.1, BR1.3 |
| frontend/src/services/api.test.ts | BDD scenarios for URL building, ack, error, validation, transport failure, protocol, timeout | FR4, BR1.3 |
| frontend/src/components/ChatWindow.test.tsx | BDD scenarios for chat UI and App→StatsPanel command wiring | US1.1, AC1.5.4 |

## Tests Written

| File | Coverage |
|------|----------|
| tests/config/test_config.py | Settings loading, dotenv precedence, secret redaction, structured logging |
| tests/models/test_models.py | Chat/command model validation, Contract 1 serialisation |
| tests/chat_input/test_chat_input.py | AC1.1.1–AC1.1.5, empty/UTF-8/unknown/overlong input, error mapping |
| tests/agent_command/test_agent_command.py | JSON/fenced/free-form translation, rephrase errors, retry, real-client fallback |
| tests/agent_command/test_agent_command_speed.py | AC1.2.1–AC1.2.3, invalid/missing speed |
| tests/agent_command/test_agent_command_color.py | AC1.3.1–AC1.3.3, invalid/missing color |
| tests/robot_command/test_robot_command.py | BLE write, connect, reconnect-retry, callback retry, missing bleak |
| tests/robot_command/test_robot_command_speed.py | AC1.2.1–AC1.2.3 over BLE |
| tests/robot_command/test_robot_command_color.py | AC1.3.1–AC1.3.3 over BLE |
| tests/main/test_main.py | `/health`, ack/error envelopes, disconnect, SPA response, route registration |
| tests/integration/test_walking_skeleton.py | chat → agent → BLE → ack + status walking skeleton, and no-BLE-on-error path |

Every module has a happy path plus at least two error/edge scenarios, written in
Given/When/Then form before the implementation.

## Key Decisions

- **LLM boundary**: `ModelClient.complete()` protocol; production client lazily imports
  Deep Agents and falls back to a direct `ChatOpenAI` invocation. The API key is
  instance-only and never logged. Tests inject scripted clients — no key or network.
- **BLE boundary**: `BleClient` protocol with a lazily imported `bleak` adapter.
  Commands are compact UTF-8 JSON on Nordic UART service/characteristic UUIDs
  (implementation assumption). Tests inject an in-memory BLE fake — no robot.
- **Error contract**: ack `{type, message, commandId, status, timestamp}` and error
  `{type:"error", errorType, message, timestamp}`; the frontend preserves the
  backend-provided error timestamp in its `ErrorReport`.
- **Frontend ownership**: U1 owns ChatWindow, `services/api.ts` and App composition;
  U3's StatsPanel/SpeedColorSelector/ErrorDisplay were imported unchanged. Both
  typed chat and selector buttons travel through the same `/ws/chat` transport.
- **Offline test strategy**: FastAPI handlers and WebSocket clients are called
  directly with fakes (no `httpx`/`websockets` installs, no live services).

## Verification

- `python3 -m pytest tests/ --cov=backend/app --cov-report=term-missing` — **100 passed**,
  total coverage **91.26%** (80% floor met). No skips, no failures.
- `npx vitest run frontend/src/components/ChatWindow.test.tsx frontend/src/services/api.test.ts` —
  **2 files passed, 17 tests passed**.
- `npm run typecheck` — clean.
- Traceability sensor for `code-generation` — `pass: true`, zero findings. NFR
  targets are workspace-root-relative paths to `nfr-design/*.md`: the code-generation
  sensor rejects the `../nfr-design/...` form as "target escapes the project directory"
  (confirmed by a direct sensor probe), so the resolving workspace-root form is used.

## Repair Note

Before this pass the backend suite had 1 failing test:
`tests/main/test_main.py::test_given_injected_callback_when_pipeline_is_built_then_contract1_wires_it`
asserted `built.sender._status_callback is received.append`. A bound method is a new
object on every attribute access, so that identity check could never pass even though
the injected callback was stored and invoked correctly. The scenario now asserts the
callback is callable, is not the no-op default, and delivers the status to the
receiving list. No production code was changed by this repair.

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before a live robot run.
- `OPENROUTER_API_KEY` must be configured in `.env` before a live agent run; the
  automated suite needs neither a key nor a robot.
- Frontend and backend run on the same machine (localhost); no cloud hosting.
- Single-user desktop application; one command at a time.
