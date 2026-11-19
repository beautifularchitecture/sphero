# Build Instructions — sphero-chat-control

Workspace root: `/home/supermind/Code/the-beautiful-architecture/sphero`

Grounded in the three units' `code-summary.md` and `unit-test-instructions.md`
files, the recorded tech-stack decisions (`u1`/`u2`/`u3` `nfr-requirements/tech-stack-decisions.md`),
and the Testing Contract in each `code-generation-plan.md`.

## 1. Prerequisites

| Requirement | Version / Note |
|---|---|
| Python | 3.14.x (`pyproject.toml` requires `>=3.14`; verified with 3.14.8) |
| `python3` on PATH | Required — this host has no `python` alias, so every Python command below uses `python3` |
| Node.js / npm | Node 26.13.0 / npm 11.20.0 (Vite 5 + Vitest 1.6) |
| BlueZ + BLE adapter | Live robot runs only (`bluetoothctl`, `hciconfig`); not needed for the test suite |
| Sphero Mini, paired | Live robot runs only |
| `.env` with `OPENROUTER_API_KEY` | Live chat runs only; never committed (`.gitignore` excludes `.env` and `.env.*`) |

## 2. Dependency installation

```bash
# Python backend (U2 today; U1 backend source is currently absent — see Known gaps)
python3 -m pip install -r requirements.txt

# Frontend + test tooling
npm install
```

`requirements.txt` currently pins only `bleak`, `fastapi`, `pytest`,
`pytest-asyncio` and `coverage`. `package.json` declares React 18, TypeScript
5.5, Vite 5.4, Vitest 1.6, Testing Library, Tailwind and jsdom, plus
`@vitest/coverage-v8@1.6.0` added during this stage so the 80% line-coverage
floor can actually be measured.

## 3. Build commands

```bash
# SPA production bundle — Vite root is frontend/, output is ../dist
npm run build

# TypeScript type-check (no emit)
npm run typecheck
```

There is no compile step for the Python packages (interpreted); the
equivalent import check is:

```bash
python3 -c "import u2_telemetry"
```

## 4. Build verification

1. `npm run build` exits 0 and writes `dist/index.html` plus `dist/assets/*.css`
   and `dist/assets/*.js`.
2. `npm run typecheck` exits 0 with no diagnostics.
3. The bundle is credential-free: `grep -rIE "OPENROUTER|api[_-]?key|sk-or-" dist frontend/src`
   returns no matches.
4. `python3 -c "import u2_telemetry"` exits 0.

## 5. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `python: command not found` | No `python` alias on this host | Run `python3` instead (recorded unit commands were normalised this way) |
| `ERROR: file or directory not found: tests/` | U1 backend/tests were never generated (see Known gaps) | Not fixable in this stage; it is a Code Generation loop-back |
| `Failed to open robot-state WebSocket connection DOMException` in Vitest output | `useRobotStateConnection` builds `new WebSocket('/ws/robot-state')` with a relative URL; jsdom/browsers reject non-`ws://` URLs | Test files that mount the panel replace `global.WebSocket`; the production defect itself is a Code Generation fix |
| Vitest exits non-zero with "coverage provider not found" | `@vitest/coverage-v8` missing | `npm install --save-dev @vitest/coverage-v8@1.6.0` (already applied) |
| `pytest-asyncio` fixture-scope deprecation warning | Plugin default changed | Harmless; pin `asyncio_default_fixture_loop_scope` when the suite is modernised |
| `npm run build` cannot find `index.html` | Vite root is `frontend/` | Run from the workspace root, not from `frontend/` |

## 6. Known gaps at this stage

- **U1 backend and U1 frontend source do not exist.** `backend/`, `tests/`,
  `frontend/src/components/ChatWindow.tsx` and `frontend/src/services/api.ts`
  are listed in `u1-chat-command-core/code-generation/code-summary.md` and
  `source-manifest.json` but were never written to disk. The U1 test command
  (`pytest tests/ --cov=backend/app`) therefore fails at collection.
- **U3 WebSocket URL is relative.** `frontend/src/hooks/useRobotStateConnection.ts`
  calls `new WebSocket(WS_ROBOT_STATE_PATH)` with `WS_ROBOT_STATE_PATH = '/ws/robot-state'`.
  No test asserts an absolute `ws://` URL; the constructor throws in jsdom and
  in browsers.
- **No real-browser runner.** All UI checks run in jsdom (Vitest); there is no
  Playwright/Chromium run in this plan.
