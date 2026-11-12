# Code Generation Plan — u2-telemetry

Grounded in functional-spec [functional-spec], rules [rules], entities [entities], contract-summary [contract-summary], NFR design [performance-design, security-design, scalability-design, reliability-design, observability-design, logical-components], infrastructure-specification [infrastructure-specification], unit-of-work [unit-of-work], requirements [requirements], and infrastructure-design [infrastructure-specification].

## Summary

- Builds: The U2 RobotTelemetry Python service — BLE telemetry reception, RobotState normalization, RobotStateChanged event publishing, connection error handling, and CommandExecutionStatus callback from U1.
- Touches: New Python service files under the workspace root for u2-telemetry (BLE listener, normalizer, event publisher, callback handler), plus pytest test files and configuration.
- Tests: ~5-8 BDD scenario unit tests per component (Standard strategy), happy path plus at least two error/edge cases each, 80% line coverage floor.

## Implementation Steps

| Step | Checkbox | Story | Description |
|------|----------|-------|-------------|
| 1 | [x] | US1.4 | Project structure and production configuration skeleton for u2-telemetry (Python package layout, pyproject.toml, entry point). |
| 2 | [x] | US1.4 | Bootstrap the minimal test runner/configuration (pytest + coverage.py) and record the exact unit-scoped command. |
| 3 | [x] | US1.4 | Behavior scenarios — define executable Given/When/Then examples for telemetry reception, normalization, publishing, error handling, and callback before implementation. |
| 4 | [x] | US1.4 | Feature slice — implement the RobotTelemetry service: BLE listener, RobotState normalization (lenient), event publisher, U1 callback handler, connection error handler. |
| 5 | [x] | US1.4 | Behavior scenarios — run the scenarios until they pass. |
| 6 | [x] | US1.4 | Feature slice — refactor while the scenarios stay green. |
| 7 | [x] | US1.4 | Environment/build configuration (systemd unit, requirements.txt, deployment notes). |
| 8 | [x] | US1.4 | Documentation and traceability (code-summary.md, source-manifest.json, traceability.json written by conductor; code-side traceability via BR/Contract/NFR references in comments). |

## Testing Contract

The following Testing Contract block is rendered by `aidlc engine testing-posture render` and must be preserved verbatim. Its `contract_sha256` is the plan-approval fingerprint; do not edit the block or its hash.

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

## Story-to-Code-Step Traceability

- **US1.4** (Stats panel observability — telemetry reception part, AC1.4.1–AC1.4.2): Steps 1–8 implement the RobotTelemetry service that receives BLE telemetry, normalizes it into RobotState, and publishes RobotStateChanged events per Contract 2 for U3 StatsDisplay.

## Measurable Quality Targets

- **80% line coverage** (NFR7, mvp scope floor, additive — may not be weakened)
- **BDD methodology** (Given/When/Then scenarios first, then implement, then run tests)
- **5-8 tests per component** (Standard strategy)
- **Happy path plus at least two error/edge cases per module**
- **CI execution before merge** (failure blocks merge)
