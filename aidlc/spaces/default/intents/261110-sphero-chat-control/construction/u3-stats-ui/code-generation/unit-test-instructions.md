# Unit Test Instructions — u3-stats-ui

## Test Framework Setup and Configuration

- **Runner**: Vitest + React Testing Library (frontend stack fixed for the project, NFR6).
- **Methodology**: BDD — scenarios written in Given/When/Then first, then implemented, then run (NFR8, team practice).
- **Configuration**: `vitest.config.ts` at workspace root with the React plugin and jsdom environment; test files co-located with components under the frontend source tree, matched by the u3-stats-ui unit filter.
- **Strategy**: standard — 5–8 tests per component, plus integration test stubs for key boundaries (WebSocket telemetry → UI render; SpeedColorSelector → chat-command callback).
- **Coverage floor**: 80% line coverage for U3 frontend modules, enforced by Build and Test on the full suite and not weakenable to make this stage pass.

## How to Run THIS UNIT's Tests

Run the exact unit-scoped command (scoped to u3-stats-ui test files only — never a bare project-wide command):

```
vitest run --reporter=verbose <u3-stats-ui test file paths>
```

Replace `<u3-stats-ui test file paths>` with the exact test file paths for the u3-stats-ui components (StatsPanel, ConnectionStatus, SpeedColorSelector, ErrorDisplay, LanRiskBanner, RobotStateDisplay, useRobotStateConnection hook). Build and Test executes every unit's commands, so this command must be unit-scoped to avoid rerunning the whole suite once per unit.

The command is runnable before the first test-first cycle (runner bootstrapped in plan Step 2). A Red/Green step is invalid if no runnable command exists.

## Expected Coverage Targets

- 80% line coverage floor for U3 frontend modules (NFR7 scope floor, additive to the standard strategy).
- The floor is measured by Build and Test on the full assembled test suite; a unit-scoped run does not judge it. If a run's coverage-threshold exit occurs with every selected test passing, record it with this unit's test results — it is not a failed test. Never change the threshold to make a unit's run pass.

## Mocking / Stubbing Guidance

- Mock the native `WebSocket` for `useRobotStateConnection` tests: simulate open, message (valid and malformed JSON), close, and error events; assert reconnect backoff schedule (1s/2s/4s/8s capped at 30s), attempt counter, stale marker, and event counter behavior.
- Stub `onSendChatCommand` in `SpeedColorSelector` tests; assert it is called with `set speed <level>` / `set color <color>` exactly.
- Render every `RobotState` value and error message as React-escaped text; assert no `dangerouslySetInnerHTML` and no raw HTML injection path.
- Do not log telemetry payloads; assert `console.error` receives non-payload diagnostics only for socket failures and dropped malformed frames.

## Test Data Management

- Use valid `RobotState` payloads matching Contract 2 (required `timestamp: string`; optional `direction`, `orientation`, `color`, `position`, `connectionStatus`).
- Include missing-field and explicit-`null` cases (rendered as dashes per BR1.5.3 / NFR1.5).
- Include malformed/non-JSON and schema-mismatched frames (dropped, not rendered).
- Each module covers the happy path plus at least two error/edge cases (team test pattern).