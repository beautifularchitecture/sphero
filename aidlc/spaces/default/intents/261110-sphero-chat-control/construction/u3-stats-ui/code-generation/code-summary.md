# Code Summary — u3-stats-ui (Code Generation)

## Unit

**u3-stats-ui** — React + TypeScript + Vite + Tailwind CSS SPA stats panel (kind: ui, complexity: M). Renders the robot's current state (direction, orientation, color, position, timestamp) and connection status on the stats panel, subscribes to RobotState events from U2 over `/ws/robot-state` (Contract 2), handles partial telemetry, and renders inline speed/color selector buttons that emit chat commands to U1. Served as static files by U1's FastAPI backend.

Stories: US1.4 (stats panel observability, AC1.4.1–AC1.4.2), US1.5 (error display in chat UI, AC1.5.2–AC1.5.4), US1.2/US1.3 (speed/color command selectors, BR1.5.5).

## What was built

### Components (under `frontend/src/components/`)
- **StatsPanel.tsx** — container. Owns the `useRobotStateConnection` WebSocket subscription and composes `LanRiskBanner` (always visible), `ConnectionStatus`, `RobotStateDisplay`, the event counter / last-updated / stale indicators, `SpeedColorSelector`, and (when provided) `ErrorDisplay`.
- **RobotStateDisplay.tsx** — renders direction, orientation, color, position, timestamp. Missing/null fields render as dashes; orientation numbers render with a degree suffix (e.g. `45°`); pre-formatted strings from the hook render as-is (no double-formatting). All values are React-escaped text.
- **ConnectionStatus.tsx** — connection state indicator: connected / disconnected / pairing / error / reconnecting (attempt N), with colored dot and optional stale badge.
- **LanRiskBanner.tsx** — always-visible, non-dismissible LAN-risk banner (static in-repo copy, no dismiss control, content never sourced from network payloads).
- **ErrorDisplay.tsx** — renders an error report (type, message, timestamp) as React-escaped text; renders nothing when there is no error; no `dangerouslySetInnerHTML`.
- **SpeedColorSelector.tsx** — inline speed (low/medium/high) and color (red/blue/green) buttons; emits `set speed <level>` / `set color <color>` exactly through the `onSendChatCommand` callback; disabled when no handler is supplied; does not call U1 directly.

### Hook (`frontend/src/hooks/useRobotStateConnection.ts`)
- Native `WebSocket` subscription to `/ws/robot-state` initiated on mount.
- Exponential reconnect backoff 1s / 2s / 4s / 8s capped at 30s, tracked via a ref (not React state) so closes outside React's act/sync flush still observe the correct attempt count.
- JSON parse + shape validation (`isValidRobotState`): required `timestamp: string`; optional `direction`/`color`/`position` (string), `orientation` (number), `connectionStatus` (string); missing/explicit-null tolerated.
- Malformed/non-JSON/shape-mismatched frames dropped with a non-payload `console.error` diagnostic; state, counter, and last-updated untouched; stale state not cleared.
- Event counter and `lastUpdatedAt` updated on every valid event.
- Stale marker clears on the **first new valid event after reconnect**, not on socket open.
- Socket teardown on unmount; reconnect timer cleared; no thrown errors in teardown paths.

### Types & constants (`frontend/src/types.ts`, `frontend/src/constants.ts`)
- `RobotStatePayload`, `RobotStateView`, `ConnectionView`, `ErrorReport`, `SpeedColorSelectorProps`, `StatsPanelProps`.
- `WS_ROBOT_STATE_PATH = '/ws/robot-state'`, `LAN_RISK_BANNER_TEXT`, `DASH = '-'`, `RECONNECT_BASE_DELAY_MS = 1000`, `RECONNECT_MAX_DELAY_MS = 30000`.

### Test infrastructure
- `vitest.config.ts` (workspace root): React plugin, jsdom environment, globals, `include: ['frontend/src/**/*.test.{ts,tsx}']`, `setupFiles: ['./frontend/src/test-setup.ts']` (registers `@testing-library/jest-dom` matchers).
- `frontend/src/test-setup.ts` — imports `@testing-library/jest-dom`.
- `frontend/src/test-utils/mockWebSocket.ts` — `MockWebSocket` with `simulateOpen/simulateMessage/simulateError/close`, static `instances` registry and `reset()`.
- One test file per component plus two integration stubs (WebSocket→UI telemetry path; SpeedColorSelector→chat-command path). All scenarios written in Given/When/Then (BDD).

### Build
- `vite.config.ts` (workspace root): `root: 'frontend'`, React plugin, `build.outDir: '../dist'`, `emptyOutDir: true`.
- `npm run build` (`vite build`) produces `dist/index.html` + `dist/assets/*.css` + `dist/assets/*.js`, consumable by U1's FastAPI static serving.

## How tests run

Exact unit-scoped command (u3-stats-ui test files only, never a bare project-wide command):

```
vitest run --reporter=verbose <u3-stats-ui test file paths>
```

Result: **45 tests passed across 9 test files**; `tsc --noEmit` clean; `vite build` produced `dist/` successfully.

## Traceability

Every assigned acceptance criterion, business rule, and non-functional requirement is mapped to implementation and test files in `traceability.json` (same directory).

Key mappings:
- **AC1.4.1** (US1.4): `useRobotStateConnection.ts`, `StatsPanel.tsx`, `RobotStateDisplay.tsx`, `ConnectionStatus.tsx` — verified by the hook, StatsPanel, RobotStateDisplay, ConnectionStatus, and WebSocket→UI integration tests.
- **AC1.4.2** (US1.4): `LanRiskBanner.tsx`, `StatsPanel.tsx`, `ConnectionStatus.tsx`, `vitest.config.ts`, `vite.config.ts` — verified by LanRiskBanner, StatsPanel, ConnectionStatus tests.
- **AC1.5.2–AC1.5.4** (US1.5): `ErrorDisplay.tsx`, `StatsPanel.tsx` — verified by ErrorDisplay and StatsPanel tests (escaped type/message/timestamp; HTML escaping).
- **BR1.5.5** (US1.2/US1.3): `SpeedColorSelector.tsx`, `StatsPanel.tsx` — verified by SpeedColorSelector, speed-color-chat integration, and StatsPanel tests.
- **NFR1.2** (safe rendering): all components use React-escaped text, no `dangerouslySetInnerHTML` — verified by ErrorDisplay and RobotStateDisplay HTML-escape tests.
- **NFR1.4** (LAN risk banner): `LanRiskBanner.tsx` always visible, non-dismissible — verified by LanRiskBanner tests.
- **NFR1.5** (dashes for missing/null): `RobotStateDisplay.tsx`, `useRobotStateConnection.ts`, `constants.ts` — verified by dash tests.
- **NFR3.4** (backoff 1/2/4/8 capped 30s): `useRobotStateConnection.ts` — verified by the backoff schedule test.
- **NFR3.5** (stale clears on first valid event): `useRobotStateConnection.ts` — verified by the stale-marker test.
- **NFR6** (Vitest + RTL): `vitest.config.ts`, test setup, mock utility.
- **NFR7** (80% coverage floor): enforced by Build and Test in CI on the full suite; not weakened for this stage.
- **NFR8** (BDD methodology): every test is a Given/When/Then scenario.

## Security notes

- No `dangerouslySetInnerHTML` anywhere; all telemetry and error strings render as React-escaped text.
- No frontend secrets: `OPENROUTER_API_KEY` stays in U1's `.env`; U3 never calls OpenRouter. The `dist/` bundle contains no credentials.
- `LanRiskBanner` documents the accepted unauthenticated-LAN-WebSocket risk; it is always visible and non-dismissible.
- CI deterministic bundle secret scan gate (NFR1.3) is enforced outside this stage.

## Step status (per code-generation-plan.md)

Steps 1–8 complete:
1. Project structure and production configuration skeleton — done
2. Test runner/bootstrap and unit-scoped command — done
3. Behavior scenarios (Given/When/Then) — done
4. Feature slice implementation — done
5. Behavior scenarios run until green (BDD green) — done: 45/45 passing
6. Refactor while green — done (fixed jest-dom registration, orientation degree formatting, backoff stale-closure, pre-existing ConnectionStatus type errors; `tsc --noEmit` clean, 45/45 still passing)
7. Vite build producing `dist/` — done
8. Documentation and traceability — done (this file + `traceability.json`)
