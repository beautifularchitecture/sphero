# Test Results — sphero-chat-control

Replay run: 2026-11-19T20:22Z · Stage: `build-and-test` (3.6) · Test Strategy: Standard · Mode: `Modify` on loop-back 2 re-entry (Redo forbidden — it would erase the Loop-Back Log)

## 1. Commands and outcomes (fresh replay)

| # | Command | Exit | Result | Notes |
|---|---------|------|--------|-------|
| 1 | `npm run build` | 0 | **PASS** | 41 modules; `dist/index.html` 0.40 kB, CSS 8.40 kB, JS 153.44 kB |
| 2 | `npm run typecheck` (`tsc --noEmit`) | 0 | **PASS** | no diagnostics |
| 3 | `python3 -m pytest tests/ --cov=backend/app --cov-report=term-missing` | 0 | **PASS** | 100 passed, 0 failed, 0 skipped; 91.26% coverage |
| 4 | `python3 -m pytest u2_telemetry/ -v --cov=u2_telemetry --cov-report=term-missing` | 0 | **PASS** | 53 passed, 0 failed, 0 skipped; 94.42% coverage |
| 5 | `npx vitest run --reporter=dot` | 0 | **PASS** | 11 files, 65 tests passed, 0 failed, 0 skipped; no `DOMException` stderr |
| 6 | `npx vitest run --coverage --coverage.provider=v8 --coverage.include='frontend/src/**/*.{ts,tsx}' --coverage.exclude='frontend/src/**/*.test.{ts,tsx}' --coverage.exclude='frontend/src/test-utils/**' --coverage.exclude='frontend/src/test-setup.ts' --coverage.reporter=text` | 0 | **PASS** | 94.02% lines, 85.63% branches, 97.56% funcs |
| 7 | `aidlc engine sensor-traceability --stage build-and-test` | 0 | **PASS** | `pass: true`, `uncovered: []`, 30 IDs covered |

Command normalisation: the recorded U1/U2 instruction files use `python`, which is
not on PATH on this host (`/usr/bin/python3` only). The equivalent `python3`
commands were run once each; no recorded test was skipped.

Deduplication: the U1 command is project-scoped (`tests/` + `backend/app`) and the
U2 command is unit-scoped (`u2_telemetry/`); they are not identical, so both ran.
The U3 instruction file carries a placeholder command
(`vitest run --reporter=verbose <u3-stats-ui test file paths>`); the actual test
file paths were supplied and the full assembled frontend suite was run once.

## 2. Failures

**None on this replay.** The first-pass failures F1–F4 are all resolved:

- **F1 (U1 absent)** — resolved in loop-back 1: the six backend modules, `/health`
  and the three pytest suites now exist; `pytest tests/` collects and passes 100
  tests at 91.26% coverage.
- **F2 (U3 relative WebSocket URL)** — resolved in loop-back 2:
  `robotStateWebSocketUrl()` in `frontend/src/constants.ts` builds an absolute
  `ws://`/`wss://` URL from `window.location`; the hook uses it and three BDD
  tests assert the scheme, host and path. The jsdom `DOMException` stderr is gone.
- **F3 (U3 no chat transport)** — resolved in loop-back 1: `ChatWindow.tsx` and
  `services/api.ts` exist and `App.tsx` passes `onSendChatCommand`.
- **F4 (traceability fail)** — resolved: the traceability sensor now reports
  `pass: true` with no uncovered IDs (NFR5 settled as `N/A`-with-reason and NFR6
  as `OK` → `frontend/src/test-setup.ts` in U3 Code Generation).

## 3. Coverage report (fresh replay)

### U1 — `coverage.py` (branch mode)

```
TOTAL   586 stmts   40 miss   112 branch   15 partial   91.26%
Required test coverage of 80.0% reached. Total coverage: 91.26%
```

Per-module low point: `agent_command.py` 84.80%; all modules above the 80% floor.
100 passed.

### U2 — `coverage.py` (branch mode)

```
TOTAL  1547 stmts   65 miss   156 branch   24 partial   94.42%
Required test coverage of 80.0% reached. Total coverage: 94.42%
```

Lowest module: `service.py` 84.78%; all measured source above 80%. 53 passed.

### U3 — `@vitest/coverage-v8`

```
All files  | 94.02 stmts | 85.63 branch | 97.56 funcs | 94.02 lines
src/App.tsx 97.36 lines; components/* 100 lines; hooks/…Connection 88.60 lines;
src/services/api.ts 94.04 lines; src/main.tsx 0 (entrypoint, not unit-tested)
```

Whole assembled frontend at 94.02% lines — above the 80% floor. 65 passed.

## 4. Finalized Target Verification Matrix

Full source/expected columns are in `build-and-test-summary.md` §4. This is the
same matrix, finalised with actual values and verdicts on the replay. Every
target that was formerly `Not Met` is now `Met`. The remaining `Unverified` rows
are evidence-availability gaps (no real browser engine; no performance-validation
stage scheduled; no Sphero hardware), not defects — all are surfaced at the gate.

| Target ID | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|
| NFR4.1–NFR4.4, NFR2.1, NFR2.2, NFR3.1–NFR3.6, NFR7.1, NFR7.3, NFR8.1, SCA-4 (u1) | Chat→robot command path, `/health`, error/logging and retry paths implemented and tested | `pytest tests/` 100 passed; `backend/app/*.py` | — | Met |
| NFR4.5 (u1) | Latency risk documented with owner | U1 performance-requirements §NFR4.5 | — | Met |
| NFR9.1 (u1) | Input validation implemented and tested | `tests/chat_input/test_chat_input.py`, `tests/models/test_models.py` | — | Met |
| NFR9.2 (u1) | `.env` untracked and ignored; no secret in bundle | `git ls-files`, grep | — | Met |
| NFR9.3 (u1) | No auth layer; accepted LAN risk recorded | source + `LanRiskBanner` | — | Met |
| SCA-1–SCA-3 (u1) | Single-user/single-robot/one-command constraints hold by design | requirements + design | — | Met |
| NFR7.2 (u1), NFR7.2 (u3), CI obligation | CI not yet set up; `ci-pipeline` checkbox `[ ]`, still ahead in the plan | `aidlc-state.md` | ci-pipeline | N/A |
| NFR4.1–NFR4.4 (u1), NFR4.1–NFR4.3 (u2), NFR2.1 (u2) | No timing/hardware evidence; no performance-validation stage scheduled | behavioural suites; BLE mocked; performance-validation `[S]` | — (no performance-validation stage scheduled) | Unverified |
| NFR2.3 (u2) | 3-attempt bound and retry bookkeeping pass | `test_ble_listener.py`, `test_connection_handler.py` | — | Met |
| NFR2.4 (u2) | Degradation and correlation paths pass | `test_callback_handler.py`, `test_service.py` | — | Met |
| NFR4.6 (u2) | Partial/missing telemetry yields placeholders | `test_normalizer.py` | — | Met |
| NFR2.2 (u2) | No secrets in U2 | source grep | — | Met |
| NFR3.1 (u2) | Error-only logging | source (`connection_handler.py`, `event_bus.py`) | — | Met |
| NFR3.2 (u2) | U2 signals errors; U1 chat transport now renders them | `test_service.py`; `ChatWindow.tsx` + `App.tsx` | — | Met |
| NFR3.3, NFR4.4, NFR4.5 (u2) | Publish/subscribe, single robot, single consumer pass | `test_event_bus.py`, `test_event_publisher.py`, `test_service.py` | — | Met |
| NFR7.1 (u2) | 94.42% | pytest coverage run | — | Met |
| NFR8.1 (u2) | BDD scenarios | test sources | — | Met |
| NFR3.1 (u3) | Hook builds an absolute `ws://`/`wss://` URL from `window.location`; no `DOMException` | `robotStateWebSocketUrl()` in `constants.ts`; hook + 3 absolute-URL tests | — | Met |
| NFR3.2, NFR3.3, NFR3.4, NFR3.5 (u3) | Behaviour asserted in jsdom only; no real browser engine ran it | hook + panel tests (jsdom) | — | Unverified |
| NFR1.2 (u3) | Escaped rendering, no raw HTML | `ErrorDisplay`/`RobotStateDisplay` tests; grep | — | Met |
| NFR1.3 (u3) | No secrets in SPA/bundle | grep | — | Met |
| NFR1.4 (u3) | Banner always visible, non-dismissible | `LanRiskBanner.test.tsx` | — | Met |
| NFR1.5 (u3) | Missing/null → dash | `RobotStateDisplay`, `StatsPanel`, hook tests | — | Met |
| NFR7.1 (u3) | 94.02% | vitest coverage run | — | Met |
| NFR8.1 (u3), NFR6, NFR5 | BDD, existing runners, usable UI | test sources; components; `test-setup.ts` | — | Met |
| Standard strategy obligation | U1/U2/U3 unit + key-boundary integration tests all present and green | 100 + 53 + 65 tests, all exit 0 | — | Met |
| 80% project floor | U1 91.26%, U2 94.42%, U3 94.02% | coverage runs | — | Met |

## 5. Failure handling

### Rung 1 — in-stage fixes

No in-stage fix was needed on this replay; all prior in-stage fixes
(`@vitest/coverage-v8` devDependency, `python3` in place of `python`) are retained.

### Rung 2 — diagnosis and impact estimate

The first-pass diagnosis and impact estimates are preserved in the Loop-Back Log
below. Both sanctioned loop-backs have now been executed: loop-back 1 repaired U1
(and the U3 chat transport), loop-back 2 repaired the U3 absolute-WebSocket-URL
defect and settled NFR5/NFR6. Every `Not Met` target has a `Met` replacement.

### Rung 3 — autonomous bounded loop-back

Both loop-backs used the engine-issued jump commands and recorded deterministic
`Modify` artifact-reuse decisions. The remaining `Unverified` targets have no
identifiable fix in a swappable dimension (hardware latency needs a robot and a
performance-validation stage; browser behaviour needs a real browser engine), so
they are surfaced at the approval gate rather than driving a third loop-back.

## 6. Loop-Back Log

### Loop-back 1 — 2026-11-15T21:51:37Z

- **Diagnosis:** Build and Test cannot pass. The U1 test command exits 4 with
  `tests/` missing: `u1-chat-command-core` generated only plan/summary/
  traceability/manifest/test-instruction artefacts, so no `backend/app` source,
  no `/health`, no chat UI and no U1 tests exist. Separately, the U3 hook builds
  `new WebSocket('/ws/robot-state')` from a relative URL, which throws in jsdom
  and in browsers, so the panel cannot receive telemetry in production even
  though 45 mocked-WebSocket tests pass. `App.tsx` also passes no
  `onSendChatCommand`, so the selector buttons are disabled in the shipped app.
  Cross-unit traceability reports 21 uncovered IDs.
- **Root-cause stage:** code-generation (`u1-chat-command-core`,
  `u3-stats-ui`).
- **Planned fix:** (U1) implement the planned backend modules, `/health`,
  structured error logging and the three pytest suites with injectable LLM/BLE
  boundaries; add the runtime dependencies; reconcile frontend ownership with
  U3 (keep U3's components, add ChatWindow + `services/api.ts` + App wiring).
  (U3) build an absolute `ws://`/`wss://` URL from `window.location` and assert
  it in a test; accept the chat-command callback from the U1 entrypoint.
  (U1 traceability) point NFR rows at `../nfr-design/<file>` and re-map
  FR1.1/FR1.2/FR2/AC1.1.x–AC1.3.x once code exists.
- **Estimated impact:** effort — one bounded Code Generation replay for two
  units plus two Plan Approval stops, roughly 6 backend modules, 3–5 test
  modules and 2 frontend changes; risk — medium (LLM/BLE must stay mockable, no
  OpenRouter key or robot on this host, cross-unit file ownership); financial —
  none, all local.

### Loop-back 2 — 2026-11-19T20:06:31Z

- **Diagnosis:** Loop-back 1's planned U1 repair is complete and green on a
  fresh re-run (100 pytest tests, 91.26% coverage; 62 frontend tests, 94.16%
  coverage; `npm run build` and `npm run typecheck` pass). The engine replay,
  however, reopened only `u1-chat-command-core`; `u3-stats-ui` was never
  reopened, so loop-back 1's promised U3 fix was never applied. `frontend/src/
  hooks/useRobotStateConnection.ts:150` still calls
  `new WebSocket(WS_ROBOT_STATE_PATH)` with the relative path `/ws/robot-state`,
  which the `WebSocket` constructor rejects with `DOMException` in both jsdom
  and browsers. Every `StatsPanel` mount that does not replace
  `global.WebSocket` logs `Failed to open robot-state WebSocket connection
  DOMException`, so NFR3.1 (u3) is `Not Met` and the panel cannot receive
  telemetry in production. The traceability gate still reports `NFR5` and
  `NFR6` uncovered because no Code Generation table settles them.
- **Root-cause stage:** code-generation (`u3-stats-ui`) — generated source plus
  its code-generation traceability table.
- **Planned fix:** (U3 code) build an absolute `ws://`/`wss://` URL from
  `window.location` (`wss:` on https, `ws:` otherwise) plus
  `WS_ROBOT_STATE_PATH`, use it in the hook, and add a Given/When/Then test
  asserting the constructed socket URL is absolute with the correct scheme,
  host and path. (U3 traceability) add a Code Generation `N/A`-with-reason
  coverage row for NFR5 and an `OK` row for NFR6 pointing at the real Vitest/
  RTL config files, so the build-and-test settlement gate sees them. U1 and U2
  are untouched.
- **Estimated impact:** effort — one bounded Code Generation replay for
  `u3-stats-ui` only (one hook change, one new test, two traceability rows)
  plus a fresh Plan Approval, review and checkpoint. Risk — low (local; no
  hardware or network key; jsdom `window.location` is configurable).
  Financial — none.

## 7. Readiness

All executed commands pass and every formerly-`Not Met` target is now `Met`.
`aidlc engine sensor-traceability --stage build-and-test` reports `pass: true`
with no uncovered IDs. The remaining `Unverified` rows are evidence-availability
gaps only: browser-dependent U3 targets were checked in jsdom (no real browser
engine available), and timing/hardware targets have no performance-validation
stage scheduled and no Sphero Mini attached. These are surfaced once at the
approval gate; the gate is presented on this replay.
