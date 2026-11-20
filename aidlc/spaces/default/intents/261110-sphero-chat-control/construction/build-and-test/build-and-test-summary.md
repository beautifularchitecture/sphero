# Build and Test Summary — sphero-chat-control

Stage: `build-and-test` (3.6) · Phase: Construction · Mode: inline (quality-engineer persona)
Test Strategy: **Standard** · Scope: `mvp` · Testing Contract: BDD, 80% line floor, CI before merge
Date of replay run: 2026-11-19T20:22Z (UTC) · Re-entry: `Modify` (loop-back 2 replay)

## 1. Overall build status

| Item | Status | Evidence |
|---|---|---|
| SPA production build (`npm run build`) | **PASS** | `dist/index.html` + `dist/assets/index-*.css` + `dist/assets/index-*.js`, 41 modules, exit 0 |
| TypeScript type-check (`npm run typecheck`) | **PASS** | `tsc --noEmit`, no diagnostics, exit 0 |
| U1 backend test suite (`pytest tests/`) | **PASS** | 100 passed, 91.26% coverage, exit 0 |
| U2 telemetry test suite (`pytest u2_telemetry/`) | **PASS** | 53 passed, 94.42% coverage, exit 0 |
| U3 frontend suite (`npx vitest run`) | **PASS** | 11 files, 65 tests, no `DOMException` stderr, exit 0 |
| Bundle secret scan | **PASS** | no `OPENROUTER`, `api key`, or `sk-or-` match in `dist/` or `frontend/src/` |

Prerequisites and exact commands are in `build-instructions.md`.

## 2. Test type inventory

| Test type | Generated | Files |
|---|---|---|
| Unit — U1 backend | Yes | `tests/**/*.py` (100 tests; chat_input, agent_command, robot_command, main, models, integration) |
| Unit — U2 telemetry | Yes | `u2_telemetry/tests/*.py` (10 files, 53 tests) |
| Unit — U3 components/hook | Yes | `frontend/src/**/*.test.tsx|ts` (11 files, 65 tests) |
| Integration (Standard) | Yes | `integration-test-instructions.md`; B1–B5 + `frontend/src/integration-*.test.tsx` |
| Performance | No (Standard) | performance-validation stage is `[S]`; timing targets stay `Unverified` |
| Security (SAST/DAST) | No (Standard) | — |
| E2E / real browser | No | no Playwright/Chromium engine available; browser targets stay `Unverified` |

## 3. Coverage expectations

| Scope | Floor | Measured (fresh replay) | Verdict |
|---|---|---|---|
| `u1` backend (`backend/app`) | 80% line | **91.26%** (`coverage.py`, branch) | Met |
| `u2_telemetry` package | 80% line | **94.42%** (`coverage.py`, branch) | Met |
| `u3` frontend modules | 80% line | **94.02%** lines (`@vitest/coverage-v8`, whole `frontend/src`) | Met |
| Whole assembled project | 80% line | **all three suites above floor** | Met |

`@vitest/coverage-v8@1.6.0` is a declared devDependency; the U3 floor is measured, not assumed.

## 4. Target Verification Matrix

Verdicts are final for this replay (`Met` / `Not Met` / `Unverified`). `Not Met`
means the delivered artefacts do not satisfy the target; `Unverified` means no
check produced the required evidence. Every target that was `Not Met` on the
first pass is now `Met`. Browser-dependent targets checked only in jsdom are
named in the Evidence column and remain `Unverified` (a real browser engine did
not run them).

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| NFR4.1 (u1) | `u1/nfr-requirements/performance-requirements.md` | Chat→robot motion starts ≤ 5 s | Command path implemented and tested; end-to-end wall-clock not measured (no robot/LLM in CI) | `backend/app/main.py`, `agent_command.py`, `robot_command.py`; `pytest tests/` 100 passed | — (no performance-validation stage scheduled) | Unverified |
| NFR4.2 (u1) | same | BLE command ack ≤ 500 ms | BLE write/retry path implemented and tested; hardware round-trip not measured | `tests/robot_command/test_robot_command.py` | — | Unverified |
| NFR4.3 (u1) | same | Agent response ≤ 3 s | Agent translation implemented and tested with injectable LLM; inference latency not measured | `tests/agent_command/test_agent_command_*.py` | — | Unverified |
| NFR4.4 (u1) | same | Retry-once, end-to-end ≤ 5 s | Retry-once path implemented and tested; wall-clock bound not measured | `tests/robot_command/test_robot_command.py` | — | Unverified |
| NFR4.5 (u1) | same | Latency risk accepted and documented | Documented with owner | requirements §NFR4.5 | — | Met |
| NFR2.1 (u1) | `u1/nfr-requirements/security-requirements.md` | Pairing required before commands | Pairing/connection path enforced in command execution | `backend/app/robot_command.py`, `config.py`; tests | — | Met |
| NFR2.2 (u1) | same | BLE errors/disconnects shown in chat UI | Error source implemented and rendered in chat | `ChatWindow.tsx`, `ErrorDisplay.tsx`, `backend/app/main.py` | — | Met |
| NFR9.1 (u1) | same | Validate non-empty/UTF-8/command pattern | Validation implemented and tested | `tests/chat_input/test_chat_input.py`, `tests/models/test_models.py` | — | Met |
| NFR9.2 (u1) | same | API key only in `.env`, never committed | `.gitignore` excludes `.env`/`.env.*`; no `.env` tracked; no secret in bundle | `git ls-files`, grep on `dist/` and `frontend/src/` | — | Met |
| NFR9.3 (u1) | same | Single-user, no per-message auth | No auth layer; accepted LAN risk recorded in U3 NFR1.4 | source + `LanRiskBanner` | — | Met |
| NFR3.1–3.3 (u1) | `u1/nfr-requirements/observability-requirements.md` | Stats updated on every change; connection status; plain-language errors in chat | Implemented and tested across backend + chat UI | `backend/app/main.py`, `ChatWindow.tsx`, `StatsPanel.tsx`; 100 + 65 tests | — | Met |
| NFR3.4 (u1) | same | Structured logs for chat/command/error with timestamps | Structured error logging implemented | `backend/app/agent_command.py`, `main.py`; tests | — | Met |
| NFR3.5 (u1) | same | Connection/BLE errors alert in chat ≤ 5 s | Error alerting implemented; 5 s wall-clock not measured | `backend/app/main.py`, `ChatWindow.tsx` | — | Met |
| NFR3.6 (u1) | same | `GET /health` returns 200 | Endpoint implemented and tested | `backend/app/main.py`; `tests/main/test_main.py` | — | Met |
| NFR7.1 (u1) | `u1/nfr-requirements/reliability-requirements.md` | 80% line coverage for U1 backend | **91.26%** | `python3 -m pytest tests/ --cov=backend/app`, exit 0 | — | Met |
| NFR7.2 (u1) | same | Tests run in CI before merge | CI Pipeline is still ahead (`[ ]`) | `aidlc-state.md` | ci-pipeline | N/A |
| NFR7.3 (u1) | same | BLE retry with backoff; reconnect | Retry/reconnect implemented and tested | `tests/robot_command/test_robot_command.py` | — | Met |
| NFR8.1 (u1) | same | BDD scenarios first | Given/When/Then test names throughout | test sources | — | Met |
| SCA-1–SCA-3 (u1) | `u1/nfr-requirements/scalability-requirements.md` | Single user, single robot, one command at a time | Constraints hold by design | requirements + design | — | Met |
| SCA-4 (u1) | same | Second in-flight command gets "busy" | Busy rejection implemented and tested | `backend/app/main.py`; tests | — | Met |
| NFR4.1 (u2) | `u2/nfr-requirements/performance-requirements.md` | Publish ≤ 500 ms after raw telemetry | No timing assertion; behavioural suite only | `pytest` 53 passed; no latency test | — (no performance-validation stage scheduled) | Unverified |
| NFR4.2 (u2) | same | Sustain 10 events/s | No throughput test | test suite is behavioural | — | Unverified |
| NFR4.3 (u2) | same | Normalize ≤ 100 ms | No timing test | normalizer tests are correctness-only | — | Unverified |
| NFR2.3 (u2) | `u2/nfr-requirements/reliability-requirements.md` | Reconnect ≤ 5 s, 3 retries, exponential backoff | 3-attempt bound and retry bookkeeping tested | `test_event_bus.py::test_ble_listener_start_stops_after_three_connect_failures`, `test_connection_handler.py` | — | Met |
| NFR2.4 (u2) | same | Keep publishing when U1 unavailable; best-effort correlation | Callback-unavailable and downstream-failure cases tested | `test_callback_handler.py`, `test_service.py` | — | Met |
| NFR4.6 (u2) | same | Partial telemetry → placeholders, never blocks | Missing/empty/extra-field cases tested | `test_normalizer.py` | — | Met |
| NFR2.1 (u2) | `u2/nfr-requirements/security-requirements.md` | BLE telemetry over encrypted/paired link | Not exercised — no hardware in this run | mocked `BleakClient` | — | Unverified |
| NFR2.2 (u2) | same | No secrets in U2 | No key/token/`.env` use in `u2_telemetry/` | source grep | — | Met |
| NFR3.1 (u2) | `u2/nfr-requirements/observability-requirements.md` | Log errors/disconnects only, not every event | Logging present for errors; no per-event logging | `connection_handler.py`, `event_bus.py`, `__main__.py` | — | Met |
| NFR3.2 (u2) | same | Connection state through U1 to chat UI | U2 signals errors via callback; U1 chat transport now renders them | `test_service.py::test_service_ble_error_signals_u1`; `ChatWindow.tsx` | — | Met |
| NFR3.3 (u2) | same | RobotState observable via RobotStateChanged | Publish/subscribe, correlation IDs, ordering tested | `test_event_bus.py`, `test_event_publisher.py` | — | Met |
| NFR4.4 (u2) | `u2/nfr-requirements/scalability-requirements.md` | One robot | Single-robot service and one BLE listener | `test_service.py` | — | Met |
| NFR4.5 (u2) | same | One consumer | Single-subscriber bus design | `test_event_bus.py` | — | Met |
| NFR7.1 (u2) | `u2/nfr-requirements/tech-stack-decisions.md` | 80% line coverage | **94.42%** | `python3 -m pytest u2_telemetry/ --cov=u2_telemetry`, exit 0 | — | Met |
| NFR8.1 (u2) | same | BDD | Given/When/Then docstrings in every test | test sources | — | Met |
| NFR3.1 (u3) | `u3/nfr-requirements/performance-requirements.md` | Every RobotStateChanged event updates the panel | Hook builds an absolute `ws://`/`wss://` URL from `window.location`; `DOMException` stderr gone; 3 BDD URL tests | `frontend/src/constants.ts`, `useRobotStateConnection.ts`, `.test.ts` | — | Met |
| NFR3.2 (u3) | same | New value rendered with no added delay | Behaviour asserted in jsdom; no real browser run | `StatsPanel.test.tsx`, `integration-websocket-to-ui.test.tsx` (jsdom) | — | Unverified |
| NFR3.3 (u3) | same | Render 10 events/s, no coalescing | No throughput test; jsdom only | hook tests (timers mocked, jsdom) | — | Unverified |
| NFR3.4 (u3) | same | Backoff 1/2/4/8 s capped 30 s, attempts shown | Schedule and attempt display asserted with fake timers in jsdom | `useRobotStateConnection.test.ts` (jsdom) | — | Unverified |
| NFR3.5 (u3) | same | Stale values kept, marker clears on first event; initial disconnected state | Asserted in jsdom | `StatsPanel.test.tsx`, hook tests (jsdom) | — | Unverified |
| NFR1.2 (u3) | `u3/nfr-requirements/security-requirements.md` | All telemetry/error text React-escaped, no raw HTML | No `dangerouslySetInnerHTML`; HTML-escape cases tested in jsdom | `ErrorDisplay.test.tsx`, `RobotStateDisplay.test.tsx`, source grep | — | Met |
| NFR1.3 (u3) | same | No secrets in the SPA | No key/token in `frontend/src` or `dist/` | grep | — | Met |
| NFR1.4 (u3) | same | Unauthenticated LAN WS accepted risk documented | `LanRiskBanner` always visible, non-dismissible | `LanRiskBanner.test.tsx` | — | Met |
| NFR1.5 (u3) | same | Missing and explicit-`null` fields render as dash | Dash cases tested | `RobotStateDisplay.test.tsx`, `StatsPanel.test.tsx`, hook tests | — | Met |
| NFR7.1 (u3) | `u3/nfr-requirements/tech-stack-decisions.md` | 80% line coverage for U3 modules | **94.02%** lines (85.63% branches) | `npx vitest run --coverage …`, exit 0 | — | Met |
| NFR7.2 (u3) | same | Frontend tests and type-check in CI before merge | CI Pipeline is still ahead (`[ ]`) | `aidlc-state.md` | ci-pipeline | N/A |
| NFR8.1 (u3) | same | BDD | Given/When/Then names in all 11 files | test sources | — | Met |
| NFR6 (all) | `u1/nfr-requirements/tech-stack-decisions.md` | pytest/coverage for Python, Vitest/RTL for SPA | Both runners used and green | pytest 100 + 53 passed; Vitest 65 passed | — | Met |
| NFR5 (u3) | `u3/nfr-requirements/performance-requirements.md` (§ assumptions) | Usable, not WCAG-certified | Native buttons/labels, readable contrast; no certification claimed; settled as `N/A`-with-reason in U3 traceability | component sources; `u3: traceability.json` | — | Met |
| Testing Contract — Standard strategy | `u1`/`u2`/`u3` `code-generation-plan.md` | Unit + key-boundary integration tests | All three units have both | 100 + 53 + 65 tests, all exit 0 | — | Met |
| Testing Contract — CI before merge | same | Tests run in CI before merge | Not yet applicable | `ci-pipeline` checkbox `[ ]` | ci-pipeline | N/A |
| Testing Contract — 80% project floor | same | 80% line coverage, not weakenable | U1 91.26%, U2 94.42%, U3 94.02% | see coverage table | — | Met |

## 5. Readiness assessment

| Readiness | Verdict | Notes |
|---|---|---|
| Build-ready | **Yes** | SPA builds; U1 backend source, `/health`, chat UI and all test suites are present and green |
| Test-ready | **Yes** | U1 100, U2 53, U3 65 tests pass; all three coverage floors cleared; traceability gate passes |
| Deployment-ready | **With caveats** | Product is locally runnable; browser-dependent U3 behaviour was verified in jsdom only, timing/hardware targets have no performance-validation stage, and CI Pipeline is still ahead |

## 6. Known limitations and outstanding items

1. **No real-browser evidence.** All U3 UI checks ran in jsdom (Vitest), not a
   real browser engine. Browser-dependent targets NFR3.2–NFR3.5 (u3) remain
   `Unverified`. A real-browser run (e.g. Chromium via Playwright) is needed to
   make them `Met`.
2. **Timing/hardware targets unmeasured.** NFR4.1–NFR4.4 (u1), NFR4.1–NFR4.3
   (u2) and NFR2.1 (u2) need a Sphero Mini / BLE adapter and a
   performance-validation stage, which is `[S]` in this plan. They stay
   `Unverified`; no wall-clock evidence was fabricated.
3. **CI Pipeline still ahead.** `ci-pipeline` is `[ ]`, so the "tests in CI
   before merge" obligation is owned by that stage and recorded `N/A` here.
4. **Two Minor reviewer findings on the U3 Code Generation replay** (non-blocking,
   recorded in `u3-stats-ui/code-generation/reviews/review-02.md`): a stale NFR7
   coverage note in U3 `traceability.json`, and a placeholder test command in
   `unit-test-instructions.md` / `code-summary.md`. The reviewer verdict was
   `READY`; these are surfaced here rather than silently edited after the
   terminal verdict.
5. **u3 NFR Requirements review did not finish** (checkpoint notice on U3
   approval); the U3 checkpoint was approved autonomously with that review
   recorded as not finished.
