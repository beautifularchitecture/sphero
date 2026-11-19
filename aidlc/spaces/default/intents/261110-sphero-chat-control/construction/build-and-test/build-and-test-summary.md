# Build and Test Summary — sphero-chat-control

Stage: `build-and-test` (3.6) · Phase: Construction · Mode: inline (quality-engineer persona)
Test Strategy: **Standard** · Scope: `mvp` · Testing Contract: BDD, 80% line floor, CI before merge
Date of run: 2026-11-15 (UTC)

## 1. Overall build status

| Item | Status | Evidence |
|---|---|---|
| SPA production build (`npm run build`) | **PASS** | `dist/index.html` + `dist/assets/index-*.css` + `dist/assets/index-*.js`, exit 0 |
| TypeScript type-check (`npm run typecheck`) | **PASS** | `tsc --noEmit`, exit 0 |
| Python package import (`u2_telemetry`) | **PASS** | imported under Python 3.14.8 |
| U1 backend build | **NOT RUNNABLE** | `backend/` and `tests/` do not exist |
| Bundle secret scan | **PASS** | no `OPENROUTER`, `api key`, or `sk-or-` match in `dist/` or `frontend/src/` |

Prerequisites and exact commands are in `build-instructions.md`.

## 2. Test type inventory

| Test type | Generated | Files |
|---|---|---|
| Unit — U1 backend | Instruction only (no code) | `u1-chat-command-core/.../unit-test-instructions.md` |
| Unit — U2 telemetry | Yes | `u2_telemetry/tests/*.py` (10 files, 53 tests) |
| Unit — U3 components/hook | Yes | `frontend/src/**/*.test.tsx|ts` (9 files, 45 tests) |
| Integration (Standard) | Yes | `integration-test-instructions.md`; B1–B5 |
| Performance | No (Standard) | — |
| Security (SAST/DAST) | No (Standard) | — |
| E2E / real browser | No | no Playwright/Chromium in this plan |

## 3. Coverage expectations

| Scope | Floor | Measured | Verdict |
|---|---|---|---|
| `u1` backend (`backend/app`) | 80% line | not measurable — source and tests absent | Not Met |
| `u2_telemetry` package | 80% line | **96.62%** (`coverage.py`, branch) | Met |
| `u3` frontend modules | 80% line | **90.58%** lines (`@vitest/coverage-v8`, whole `frontend/src`) | Met |
| Whole assembled project | 80% line | blocked by missing U1 backend | Not Met |

`@vitest/coverage-v8@1.6.0` was added as a devDependency during this stage so the
U3 floor could be measured instead of assumed.

## 4. Target Verification Matrix

Verdicts are final for this run (`Met` / `Not Met` / `Unverified`). `Not Met`
means the delivered artefacts do not satisfy the target; `Unverified` means no
check produced evidence. Browser-dependent targets checked only in jsdom are
called out in the Evidence column.

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| NFR4.1 (u1) | `u1/nfr-requirements/performance-requirements.md` | Chat→robot motion starts ≤ 5 s | No AgentCommand/RobotCommand/app to measure; no robot or LLM run | U1 test command exit 4; `backend/` absent | — (no validation stage scheduled) | Not Met |
| NFR4.2 (u1) | same | BLE command ack ≤ 500 ms | Not measured | no BLE command implementation | — | Not Met |
| NFR4.3 (u1) | same | Agent response ≤ 3 s | Not measured | no agent implementation | — | Not Met |
| NFR4.4 (u1) | same | Retry-once, end-to-end ≤ 5 s | Not measured | no retry path | — | Not Met |
| NFR4.5 (u1) | same | Latency risk accepted and documented | Documented in requirements; no implementation to exercise | requirements file only | — | Not Met |
| NFR2.1 (u1) | `u1/nfr-requirements/security-requirements.md` | Pairing required before commands | No command path exists | `backend/` absent | — | Not Met |
| NFR2.2 (u1) | same | BLE errors/disconnects shown in chat UI | No backend error source; U3 can render an `ErrorReport` but nothing feeds it | U1 exit 4; `App.tsx` has no error wiring | — | Not Met |
| NFR9.1 (u1) | same | Validate non-empty/UTF-8/command pattern | Not implemented | `tests/` absent | code-generation (u1) | Not Met |
| NFR9.2 (u1) | same | API key only in `.env`, never committed | `.gitignore` excludes `.env`/`.env.*`; no `.env` tracked; no secret in bundle | `git ls-files`, grep on `dist/` and `frontend/src/` | — | Met |
| NFR9.3 (u1) | same | Single-user, no per-message auth | No auth layer implemented; accepted LAN risk recorded in U3 NFR1.4 | source + `LanRiskBanner` | — | Met |
| NFR3.1–3.3 (u1) | `u1/nfr-requirements/observability-requirements.md` | Stats updated on every change; connection status; plain-language errors in chat | No backend/stats producer; only U3 rendering exists | U1 exit 4 | — | Not Met |
| NFR3.4 (u1) | same | Structured logs for chat/command/error with timestamps | No backend logging | `backend/` absent | — | Not Met |
| NFR3.5 (u1) | same | Connection/BLE errors alert in chat ≤ 5 s | No error transport | `backend/` absent | — | Not Met |
| NFR3.6 (u1) | same | `GET /health` returns 200 | No FastAPI app | `backend/app/main.py` absent | — | Not Met |
| NFR7.1 (u1) | `u1/nfr-requirements/reliability-requirements.md` | 80% line coverage for U1 backend | not measurable; no source/tests | `pytest tests/ --cov=backend/app` exit 4 | — | Not Met |
| NFR7.2 (u1) | same | Tests run in CI before merge | CI not yet set up | `aidlc-state.md`: `ci-pipeline` is `[ ]` | ci-pipeline | N/A |
| NFR7.3 (u1) | same | BLE retry with backoff; reconnect | Not implemented in U1 | `backend/` absent | code-generation (u1) | Not Met |
| NFR8.1 (u1) | same | BDD scenarios first | No U1 tests | `tests/` absent | — | Not Met |
| SCA-1–SCA-3 (u1) | `u1/nfr-requirements/scalability-requirements.md` | Single user, single robot, one command at a time | Scope constraints hold by design (single process, single device config) | requirements + design | — | Met |
| SCA-4 (u1) | same | Second in-flight command gets "busy" | Not implemented | `backend/` absent | code-generation (u1) | Not Met |
| NFR4.1 (u2) | `u2/nfr-requirements/performance-requirements.md` | Publish ≤ 500 ms after raw telemetry | No timing test; no later performance-validation stage | `pytest` 53 passed, no latency assertion | — | Unverified |
| NFR4.2 (u2) | same | Sustain 10 events/s | No throughput test | test suite is behavioural | — | Unverified |
| NFR4.3 (u2) | same | Normalize ≤ 100 ms | No timing test | normalizer tests are correctness-only | — | Unverified |
| NFR2.3 (u2) | `u2/nfr-requirements/reliability-requirements.md` | Reconnect ≤ 5 s, 3 retries, exponential backoff | 3-attempt bound and retry bookkeeping tested | `test_event_bus.py::test_ble_listener_start_stops_after_three_connect_failures`, `test_connection_handler.py` (5 tests) | — | Met |
| NFR2.4 (u2) | same | Keep publishing when U1 unavailable; best-effort correlation | Callback-unavailable and downstream-failure cases tested | `test_callback_handler.py` (6 tests), `test_service.py` | — | Met |
| NFR4.6 (u2) | same | Partial telemetry → placeholders, never blocks | Missing/empty/extra-field cases tested | `test_normalizer.py` (9 tests) | — | Met |
| NFR2.1 (u2) | `u2/nfr-requirements/security-requirements.md` | BLE telemetry over encrypted/paired link | Not exercised — no hardware in this run | mocked `BleakClient` | — | Unverified |
| NFR2.2 (u2) | same | No secrets in U2 | No key/token/`.env` use in `u2_telemetry/` | source grep | — | Met |
| NFR3.1 (u2) | `u2/nfr-requirements/observability-requirements.md` | Log errors/disconnects only, not every event | Logging present for errors; no per-event logging | `connection_handler.py`, `event_bus.py`, `__main__.py` | — | Met |
| NFR3.2 (u2) | same | Connection state through U1 to chat UI | U2 signals errors via callback; U1 transport absent | `test_service.py::test_service_ble_error_signals_u1`; no U1 app | code-generation (u1) | Not Met |
| NFR3.3 (u2) | same | RobotState observable via RobotStateChanged | Publish/subscribe, correlation IDs, ordering tested | `test_event_bus.py` (8), `test_event_publisher.py` (6) | — | Met |
| NFR4.4 (u2) | `u2/nfr-requirements/scalability-requirements.md` | One robot | Single-robot service and one BLE listener | `test_service.py` | — | Met |
| NFR4.5 (u2) | same | One consumer | Single-subscriber bus design | `test_event_bus.py` | — | Met |
| NFR7.1 (u2) | `u2/nfr-requirements/tech-stack-decisions.md` | 80% line coverage | **96.62%** | `python3 -m pytest u2_telemetry/ --cov=u2_telemetry`, exit 0 | — | Met |
| NFR8.1 (u2) | same | BDD | Given/When/Then docstrings in every test | test sources | — | Met |
| NFR3.1 (u3) | `u3/nfr-requirements/performance-requirements.md` | Every RobotStateChanged event updates the panel | Production hook builds `new WebSocket('/ws/robot-state')` (relative) — throws `DOMException` in jsdom and in browsers; no test asserts an absolute `ws://` URL | `useRobotStateConnection.ts:150`; Vitest stderr `Failed to open robot-state WebSocket connection DOMException`; 45 tests pass only because WebSocket is mocked | code-generation (u3) | Not Met |
| NFR3.2 (u3) | same | New value rendered with no added delay | Behaviour asserted in jsdom; no real browser run | `StatsPanel.test.tsx`, `integration-websocket-to-ui.test.tsx` (jsdom) | — | Unverified |
| NFR3.3 (u3) | same | Render 10 events/s, no coalescing | No throughput test; jsdom only | hook tests (timers mocked) | — | Unverified |
| NFR3.4 (u3) | same | Backoff 1/2/4/8 s capped 30 s, attempts shown | Schedule and attempt display asserted with fake timers in jsdom | `useRobotStateConnection.test.ts` | — | Unverified |
| NFR3.5 (u3) | same | Stale values kept, marker clears on first event; initial disconnected state | Asserted in jsdom | `StatsPanel.test.tsx`, hook tests | — | Unverified |
| NFR1.2 (u3) | `u3/nfr-requirements/security-requirements.md` | All telemetry/error text React-escaped, no raw HTML | No `dangerouslySetInnerHTML`; HTML-escape cases tested in jsdom | `ErrorDisplay.test.tsx`, `RobotStateDisplay.test.tsx`, source grep | — | Met |
| NFR1.3 (u3) | same | No secrets in the SPA | No key/token in `frontend/src` or `dist/` | grep | — | Met |
| NFR1.4 (u3) | same | Unauthenticated LAN WS accepted risk documented | `LanRiskBanner` always visible, non-dismissible; banner tests | `LanRiskBanner.test.tsx` (3) | — | Met |
| NFR1.5 (u3) | same | Missing and explicit-`null` fields render as dash | Dash cases tested | `RobotStateDisplay.test.tsx`, `StatsPanel.test.tsx`, hook tests | — | Met |
| NFR7.1 (u3) | `u3/nfr-requirements/tech-stack-decisions.md` | 80% line coverage for U3 modules | **90.58%** lines (86.13% branches) | `npx vitest run --coverage …`, exit 0 | — | Met |
| NFR7.2 (u3) | same | Frontend tests and type-check in CI before merge | CI not yet set up | `ci-pipeline` is `[ ]` | ci-pipeline | N/A |
| NFR8.1 (u3) | same | BDD | Given/When/Then names in all 9 files | test sources | — | Met |
| NFR6 (all) | `u1/nfr-requirements/tech-stack-decisions.md` | pytest/coverage for Python, Vitest/RTL for SPA | Both runners used and green for existing code | pytest 53 passed; Vitest 45 passed | — | Met |
| NFR5 (u3) | `u3/nfr-requirements/performance-requirements.md` (§ assumptions) | Usable, not WCAG-certified | Native buttons/labels, readable contrast; no certification claimed | component sources | — | Met |
| Testing Contract — Standard strategy | `u1`/`u2`/`u3` `code-generation-plan.md` | Unit + key-boundary integration tests | U2/U3 have both; U1 has neither | 53 + 45 tests; U1 exit 4 | code-generation (u1) | Not Met |
| Testing Contract — CI before merge | same | Tests run in CI before merge | Not yet applicable | `ci-pipeline` checkbox `[ ]` | ci-pipeline | N/A |
| Testing Contract — 80% project floor | same | 80% line coverage, not weakenable | U2 96.62%, U3 90.58%, U1 unmeasurable | see coverage table | code-generation (u1) | Not Met |

## 5. Readiness assessment

| Readiness | Verdict | Notes |
|---|---|---|
| Build-ready | **No** | SPA builds; U1 backend source is absent, so the product cannot start or serve chat |
| Test-ready | **No** | U2 and U3 suites are green; U1 has no tests and its command fails at collection |
| Deployment-ready | **No** | No backend, no CI, no host, and U3's WebSocket URL cannot connect |

## 6. Known limitations and outstanding items

1. **U1 produced artefacts, not code.** `u1-chat-command-core` wrote
   `code-generation-plan.md`, `unit-test-instructions.md`, `code-summary.md`,
   `traceability.json` and `source-manifest.json`, and its reviewer recorded
   "PASS (artifacts only)". No `backend/app/*.py` or `tests/*.py` exists in the
   repository or its history, so every U1 behavioural target is unbuilt.
2. **U3's WebSocket URL is relative.** The panel cannot connect in a real
   browser; the defect was found in the U3 code review (`R-01`) and remains open
   after checkpoint approval.
3. **U3 is not wired to a chat transport.** `App.tsx` renders `StatsPanel`
   without `onSendChatCommand`, so the speed/colour buttons are disabled in the
   shipped app. The chat window that would supply the callback belongs to U1 and
   does not exist.
4. **Cross-unit traceability fails.** `sensor-traceability` reports 21
   uncovered IDs (FR1.1, FR1.2, FR2, NFR2–NFR8, AC1.1.1–AC1.3.3). See
   `cross-unit-traceability.md`.
5. **No real-browser evidence.** All UI checks ran in jsdom (Vitest).
6. **U2 timing targets are unmeasured** (500 ms publish, 100 ms normalize,
   10 events/s). No later performance-validation stage is scheduled in this
    plan, so they stay `Unverified`.
7. **U3 reconnect/stale/throughput targets are jsdom-only** and therefore
   `Unverified` under the stage's browser-evidence rule.
