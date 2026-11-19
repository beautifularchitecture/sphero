# Test Results — sphero-chat-control

Run date: 2026-11-15 (UTC) · Stage: `build-and-test` (3.6) · Test Strategy: Standard

## 1. Commands and outcomes

| # | Command | Exit | Result | Notes |
|---|---|---|---|---|
| 1 | `npm run build` | 0 | **PASS** | 39 modules; `dist/index.html` 0.40 kB, CSS 7.76 kB, JS 149.23 kB |
| 2 | `npm run typecheck` (`tsc --noEmit`) | 0 | **PASS** | no diagnostics |
| 3 | `python3 -m pytest u2_telemetry/ -v --cov=u2_telemetry --cov-report=term-missing` | 0 | **PASS** | 53 passed, 0 failed, 0 skipped; 96.62% coverage |
| 4 | `npx vitest run --reporter=dot` (9 u3 files) | 0 | **PASS** | 9 files, 45 tests passed, 0 failed, 0 skipped |
| 5 | `npx vitest run --coverage --coverage.provider=v8 --coverage.include='frontend/src/**/*.{ts,tsx}' --coverage.exclude='frontend/src/**/*.test.{ts,tsx}' --coverage.exclude='frontend/src/test-utils/**' --coverage.exclude='frontend/src/test-setup.ts' --coverage.reporter=text` | 0 | **PASS** | 90.58% lines, 86.13% branches, 92.3% funcs |
| 6 | `python3 -m pytest tests/ --cov=backend/app --cov-report=term-missing` | **4** | **FAIL** | `ERROR: file or directory not found: tests/`; 0 collected |

Command normalisation: the recorded U1/U2 instruction files use `python`, which is
not on PATH on this host (`/usr/bin/python3` only). The equivalent `python3`
commands were run once each; no recorded test was skipped.

Deduplication: the u1 command is project-scoped (`tests/` + `backend/app`) and the
u2 command is unit-scoped (`u2_telemetry/`); they are not identical, so both ran.
The u3 instruction file carries a placeholder command
(`vitest run --reporter=verbose <u3-stats-ui test file paths>`); the nine actual
test file paths were supplied, and the run is recorded once.

## 2. Failures

### F1 — U1 test command cannot collect

```
$ python3 -m pytest tests/ --cov=backend/app --cov-report=term-missing
platform linux -- Python 3.14.8, pytest-9.2.0, pluggy-1.7.0
rootdir: /home/supermind/Code/the-beautiful-architecture/sphero
configfile: pyproject.toml
collecting ... ERROR: file or directory not found: tests/
collected 0 items
============================ no tests ran in 0.01s =============================
exit 4
```

Root cause: `u1-chat-command-core` Code Generation never wrote the implementation
or tests it lists. `backend/`, `tests/`, `frontend/src/components/ChatWindow.tsx`
and `frontend/src/services/api.ts` are absent from the working tree and from git
history (`git log --all -- backend tests` is empty). The U1 reviewer's own
"Source-existence check" recorded "PASS (artifacts only)".

### F2 — U3 WebSocket URL is relative (product defect, tests do not catch it)

`frontend/src/hooks/useRobotStateConnection.ts:150`:

```ts
socket = new WebSocket(WS_ROBOT_STATE_PATH);   // '/ws/robot-state'
```

The browser `WebSocket` constructor requires an absolute `ws://` or `wss://`
URL; a relative URL throws. jsdom also throws, which is visible in the Vitest
run as repeated `Failed to open robot-state WebSocket connection DOMException`
on every `StatsPanel` mount that does not replace `global.WebSocket`. All 45
tests pass because the socket is mocked, and no test asserts an absolute URL.
This is the still-open `R-01` Critical from the U3 code review.

### F3 — U3 entrypoint has no chat transport

`frontend/src/App.tsx` renders `<StatsPanel />` with no `onSendChatCommand`.
`SpeedColorSelector` therefore disables its buttons in the shipped app
(`R-02` in the U3 review). The chat window that should supply the callback is a
U1 deliverable and does not exist.

### F4 — Cross-unit traceability gate fails

`aidlc engine sensor-traceability --stage build-and-test` returned
`pass: false` with 21 uncovered IDs: `FR1.1`, `FR1.2`, `FR2`, `NFR2`–`NFR8`,
`AC1.1.1`–`AC1.3.3`. The same output reports U1 traceability targets
(`security-design.md`, `observability-design.md`, `performance-design.md`,
`reliability-design.md`) as non-existent because the rows carry bare filenames
that resolve relative to `code-generation/`, not `nfr-design/`. Details in
`cross-unit-traceability.md`.

## 3. Coverage report

### U2 — `coverage.py` (branch mode)

```
TOTAL   961 stmts   25 miss   44 branch   9 partial   96.62%
Required test coverage of 80.0% reached. Total coverage: 96.62%
```

Per-module low point: `__main__.py` 63.64%; `service.py` 84.78%;
`ble_listener.py` 88.89%. All above the 80% floor individually except
`__main__.py`, which is offset by the package total; the floor is defined for the
unit, not per file.

### U3 — `@vitest/coverage-v8`

```
All files          | 90.58 stmts | 86.13 branch | 92.30 funcs | 90.58 lines
 src/App.tsx       |  0.00       |  0.00        |  0.00       |  0.00 (1-9)
 src/main.tsx      |  0.00       |  0.00        |  0.00       |  0.00 (1-12)
 components/*      | 100.00      | 100.00       | 100.00      | 100.00
 hooks/…Connection | 87.50       | 82.35        | 100.00      | 87.50
```

`App.tsx` and `main.tsx` are the uncovered entrypoints (no test mounts them
directly). They are not exercised because the App has no chat transport (F3).

### U1 — not measurable

No `backend/app` source and no `tests/` tree exist.

## 4. Finalized Target Verification Matrix

Full source/expected columns are in `build-and-test-summary.md` §4. This is the
same matrix, finalised with actual values and verdicts.

| Target ID | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|
| NFR4.1–NFR4.5, NFR2.1, NFR2.2, NFR3.1–NFR3.6, NFR7.1, NFR7.3, NFR8.1, SCA-4 (u1) | Not implemented / not measurable | `pytest tests/` exit 4; `backend/`, `tests/` absent | code-generation (u1) | Not Met |
| NFR9.1 (u1) | Validation absent | `tests/` absent | code-generation (u1) | Not Met |
| NFR9.2 (u1) | `.env` untracked and ignored; no secret in bundle | `git ls-files`, grep | — | Met |
| NFR9.3 (u1) | No auth layer; accepted LAN risk recorded | source + `LanRiskBanner` | — | Met |
| SCA-1–SCA-3 (u1) | Single-user/single-robot/one-command constraints hold by design | requirements + design | — | Met |
| NFR7.2 (u1), NFR7.2 (u3), CI obligation | CI not yet set up; `ci-pipeline` checkbox `[ ]` | `aidlc-state.md` | ci-pipeline | N/A |
| NFR4.1, NFR4.2, NFR4.3, NFR2.1 (u2) | No timing/hardware evidence | behavioural suite only; BLE mocked | — (no performance-validation stage scheduled) | Unverified |
| NFR2.3 (u2) | 3-attempt bound and retry bookkeeping pass | `test_ble_listener.py`, `test_connection_handler.py` | — | Met |
| NFR2.4 (u2) | Degradation and correlation paths pass | `test_callback_handler.py`, `test_service.py` | — | Met |
| NFR4.6 (u2) | Partial/missing telemetry yields placeholders | `test_normalizer.py` | — | Met |
| NFR2.2 (u2) | No secrets in U2 | source grep | — | Met |
| NFR3.1 (u2) | Error-only logging | source (`connection_handler.py`, `event_bus.py`) | — | Met |
| NFR3.2 (u2) | U2 signals errors; no U1 transport to the UI | `test_service.py`; U1 absent | code-generation (u1) | Not Met |
| NFR3.3, NFR4.4, NFR4.5 (u2) | Publish/subscribe, single robot, single consumer pass | `test_event_bus.py`, `test_event_publisher.py`, `test_service.py` | — | Met |
| NFR7.1 (u2) | 96.62% | pytest coverage run | — | Met |
| NFR8.1 (u2) | BDD scenarios | test sources | — | Met |
| NFR3.1 (u3) | Hook uses relative `/ws/robot-state`; constructor throws | `useRobotStateConnection.ts:150`; jsdom `DOMException` | code-generation (u3) | Not Met |
| NFR3.2, NFR3.3, NFR3.4, NFR3.5 (u3) | Behaviour asserted in jsdom only | hook + panel tests | — | Unverified |
| NFR1.2 (u3) | Escaped rendering, no raw HTML | `ErrorDisplay`/`RobotStateDisplay` tests; grep | — | Met |
| NFR1.3 (u3) | No secrets in SPA/bundle | grep | — | Met |
| NFR1.4 (u3) | Banner always visible, non-dismissible | `LanRiskBanner.test.tsx` | — | Met |
| NFR1.5 (u3) | Missing/null → dash | `RobotStateDisplay`, `StatsPanel`, hook tests | — | Met |
| NFR7.1 (u3) | 90.58% | vitest coverage run | — | Met |
| NFR8.1 (u3), NFR6, NFR5 | BDD, existing runners, usable UI | test sources; components | — | Met |
| Standard strategy obligation | U2/U3 boundaries tested; U1 has no tests | 53 + 45 tests; U1 exit 4 | code-generation (u1) | Not Met |
| 80% project floor | U2 96.62%, U3 90.58%, U1 unmeasurable | coverage runs | code-generation (u1) | Not Met |

## 5. Failure handling

### Rung 1 — in-stage fixes applied (2 attempts max)

1. **Coverage provider missing** → `@vitest/coverage-v8@1.6.0` added as a
   devDependency and coverage run with explicit include/exclude. Result: the U3
   floor is now measured (90.58%) instead of unverified. Fixed in-stage.
2. **`python` not on PATH** → ran the recorded commands with `python3`. Fixed
   in-stage (environment).

No further in-stage fix exists for F1–F4: the missing backend is an entire
code-generation deliverable, and the U3 URL/wiring defects are in generated
source.

### Rung 2 — diagnosis and impact estimate

| Failure | Root cause | Root-cause stage | Identifiable fix | Estimated impact |
|---|---|---|---|---|
| F1 U1 absent | Code Generation produced only plan/summary/manifest/test-instructions; no source or tests were written | code-generation (u1) | Implement the 6 planned backend modules (`main.py`, `chat_input.py`, `agent_command.py`, `robot_command.py`, `config.py`, `models.py`), the `/health` endpoint, and the 3 planned pytest suites; add runtime deps (`langchain`, Deep Agents, OpenRouter client) with test doubles so no network/hardware is needed; reconcile U1's frontend file list with U3's existing components | Effort: one U1 code-generation replay plus a fresh Plan Approval. Risk: medium — LLM/BLE boundaries must be injectable; no OpenRouter key or robot in CI. Financial: none (local). |
| F2 U3 relative URL | Hook builds the socket from a path-only constant | code-generation (u3) | Derive `ws://`/`wss://` from `window.location` (or an injected base URL) and add a test asserting an absolute URL; keep `WS_ROBOT_STATE_PATH` for the path | Effort: small (one hook change + one test). Risk: low. |
| F3 U3 no chat transport | U1's chat window/App wiring was never generated; U3's App renders the panel alone | code-generation (u1, u3) | U1 adds `ChatWindow` + `services/api.ts` and passes `onSendChatCommand`; U3 keeps its components and accepts the prop | Effort: part of the U1 replay plus a small U3 wiring change. Risk: low–medium (cross-unit file ownership). |
| F4 Traceability fail | U1 has no implementation to trace; U1 traceability rows use bare filenames that do not resolve | code-generation (u1) | Regenerate U1 implementation + traceability with workspace-relative targets; correct the 17 NFR rows to `../nfr-design/<file>` | Effort: included in the U1 replay. Risk: low. |

### Rung 3 — autonomous bounded loop-back

Mode is `autonomous`, the bound (3) is not exhausted, and impact-estimated fixes
exist. Loop-back 1 reopens Code Generation for the units the diagnosis names:
**u1-chat-command-core** and **u3-stats-ui**. u2-telemetry keeps its work,
reviews and approvals.

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

## 7. Readiness

**Not successful.** Build PASS; U2 and U3 suites PASS; U1 command FAIL; 20+
applicable targets `Not Met`/`Unverified`; traceability gate FAIL. The
approval gate is not presented for this failed run; Code Generation reopens
under loop-back 1.
