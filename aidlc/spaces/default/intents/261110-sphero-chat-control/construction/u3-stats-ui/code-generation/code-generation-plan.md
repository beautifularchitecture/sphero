# Code Generation Plan — u3-stats-ui

## Summary

- Builds: the u3-stats-ui React + TypeScript + Vite SPA stats panel (StatsPanel, LanRiskBanner, ConnectionStatus, ErrorDisplay, SpeedColorSelector, RobotStateDisplay) plus the useRobotStateConnection WebSocket hook, served as static files by U1's FastAPI backend.
- Touches: frontend components, the WebSocket hook, vitest config, and component tests under the workspace root (frontend code only); plan artefacts live in this record dir.
- Tests: standard strategy, ~5–8 tests per component across ~7 components (unit + integration at key boundaries), BDD Given/When/Then, 80% line coverage floor enforced by Build and Test on the full suite.

## Story-to-Code Traceability

| Plan Step | Story | AC | What it implements |
|---|---|---|---|
| Step 1 | US1.4 | AC1.4.2 | Project skeleton and vitest setup for the stats panel |
| Step 2 | US1.4 | AC1.4.2 | Test runner config and the exact unit-scoped test command |
| Step 3 | US1.4 | AC1.4.1, AC1.4.2 | BDD scenarios: telemetry render, connection status, stale/missing fields |
| Step 3 | US1.5 | AC1.5.2–AC1.5.4 | BDD scenarios: error message display in chat UI |
| Step 4 | US1.4 | AC1.4.1 | StatsPanel, RobotStateDisplay, ConnectionStatus, LanRiskBanner components |
| Step 4 | US1.2, US1.3 | BR1.5.5 | SpeedColorSelector emitting set speed/color chat commands |
| Step 4 | US1.4 | AC1.4.1 | useRobotStateConnection hook: WebSocket subscribe, reconnect backoff, parse/validate |
| Step 5 | US1.4 | AC1.4.1, AC1.4.2 | Run all BDD scenarios until green |
| Step 6 | US1.4 | AC1.4.1 | Refactor while scenarios stay green |
| Step 7 | US1.4 | AC1.4.2 | Vite build configuration and static bundle output |
| Step 8 | US1.4, US1.5 | AC1.4.1–AC1.4.2, AC1.5.2–AC1.5.4 | code-summary.md and traceability.json |

## Implementation Steps

1. [ ] Project structure and production configuration skeleton — create the frontend component files, hook, and vitest configuration scaffold for u3-stats-ui (React + TypeScript + Vite + Tailwind CSS). [US1.4 AC1.4.2]
2. [ ] Bootstrap the minimal test runner/configuration and record the exact unit-scoped command — vitest + React Testing Library configured so u3-stats-ui tests run standalone with an exact command scoped to this unit only. [US1.4 AC1.4.2]
3. [ ] Behavior scenarios — define executable Given/When/Then examples for the observable feature slice before implementation: telemetry values render on every RobotStateChanged event, missing/null fields show as dashes, connection status transitions (connected/disconnected/pairing/error), reconnect attempt indicator, stale marker clears on first valid event after reconnect, LanRiskBanner always visible and non-dismissible, SpeedColorSelector emits `set speed <level>` / `set color <color>`, ErrorDisplay renders escaped error type/message/timestamp. [US1.4 AC1.4.1–AC1.4.2; US1.5 AC1.5.2–AC1.5.4]
4. [ ] Feature slice — implement the data/repo/business/API/frontend layers: StatsPanel container, RobotStateDisplay, ConnectionStatus, LanRiskBanner, ErrorDisplay, SpeedColorSelector components and the useRobotStateConnection hook (native WebSocket, exponential backoff 1s/2s/4s/8s capped at 30s, JSON parse+shape validation, malformed-frame drop with non-payload console.error, no `dangerouslySetInnerHTML`, no frontend secrets). [US1.4 AC1.4.1–AC1.4.2; US1.2 US1.3 BR1.5.5; US1.5 BR1.5.4]
5. [ ] Behavior scenarios — run the scenarios until they pass (BDD green). [US1.4 AC1.4.1–AC1.4.2; US1.5 AC1.5.2–AC1.5.4]
6. [ ] Feature slice — refactor while the scenarios stay green; keep every measurable quality target (80% coverage, no secrets in bundle, safe escaped rendering). [US1.4 AC1.4.1–AC1.4.2]
7. [ ] Environment/build configuration — Vite build producing `dist/` static assets consumable by U1's FastAPI static serving; deterministic bundle secret scan gate enforced in CI (not in this stage). [US1.4 AC1.4.2]
8. [ ] Documentation and traceability — write code-summary.md and traceability.json mapping every assigned AC/NFR to an implementation or test file. [US1.4 AC1.4.1–AC1.4.2; US1.5 AC1.5.2–AC1.5.4]

## Testing Contract

```json
{
  "version": 1,
  "methodology": "bdd",
  "source": "team",
  "ordering": "Write scenarios in Given/When/Then first, then implement, then run tests.",
  "scope": "mvp",
  "test_strategy": "standard",
  "project_type": "greenfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra`, `classic` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    },
    {
      "layer": "team",
      "text": "- **Methodology**: bdd\n- **Methodology evidence**: BDD — write scenarios in Given/When/Then, then\n  implement to make them pass (interview Q3 answer). org.md requires the\n  testing methodology to be affirmed at practices-discovery and recorded under\n  `## Testing Posture` with explicit `Methodology` and `Ordering` fields.\n- **Ordering**: Write scenarios in Given/When/Then first, then implement, then\n  run tests.\n- **Coverage floor**: 80% line coverage (mvp scope floor per org.md; additive,\n  applies now for this intent; may not be weakened to make Build and Test\n  pass).\n- **CI execution**: tests run in CI before merge; failure blocks merge.\n- **Test patterns**: unit > integration > e2e per the test pyramid; tests\n  independent and self-contained; every module covers the happy path plus at\n  least two error/edge cases.\n- **Tooling**: pytest + coverage.py for the Python backend; language-appropriate\n  runner for the SPA frontend once its stack is selected.\n\nAffirmed at interview Q3: BDD methodology with scenarios-first ordering."
    }
  ],
  "obligations": {
    "strategy": "standard",
    "strategy_volume": [
      "Five to eight tests per component.",
      "Unit tests plus integration tests for key boundaries.",
      "Add E2E, performance, or security tests when requirements demand them."
    ],
    "scope_floor": [
      "Meet an 80% line-coverage floor.",
      "Run the selected tests in CI before merge."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "bdd",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
      "Behavior scenarios - define executable examples for the observable feature slice before implementation.",
      "Feature slice - implement the required data, repository, business, API, and frontend layers.",
      "Behavior scenarios - run the scenarios until they pass.",
      "Feature slice - refactor while the scenarios stay green.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:d5560974232222207b0b82ecca45f93aab38a44641d275cb5fc5fd5b748bed72",
  "contract_sha256": "sha256:0a7324b9ba021707c0f0dea85badebfb0ebad1b7d76c63d00296044b5b2c5184"
}
```

## Test Files and Configuration

Test files are mandatory in this plan. Per the standard strategy, there is one test file per component (~5–8 tests each) plus integration test stubs for key boundaries (WebSocket→UI telemetry path, SpeedColorSelector→chat-command path). Coverage floor: 80% line coverage for U3 frontend modules, enforced by Build and Test on the full suite and not weakenable to make this stage pass. The unit-scoped test command is recorded in `unit-test-instructions.md` and is scoped to u3-stats-ui test files only (never a bare project-wide `npm test`).