# Code Generation Plan — u1-chat-command-core

Grounded in functional design [functional-spec], requirements [requirements], unit-of-work [unit-of-work], contract design [contract-summary], NFR design [nfr-design], and tech stack decisions [tech-stack-decisions].

## Plan Summary

- Builds: chat input endpoint, AI agent translation service, Bluetooth LE robot command sender, chat UI, stats panel UI, websocket integration
- Touches: backend app package, frontend React SPA package
- Tests: pytest + coverage.py for Python backend; Vitest + React Testing Library for React SPA

## User Story Mapping

| Story | AC | Implementation Files | Test File(s) |
|-------|-----|---------------------|--------------|
| US1.1 | AC1.1.1–AC1.1.5 | backend/app/chat_input.py, backend/app/agent_command.py, backend/app/robot_command.py, backend/app/models.py | tests/chat_input/test_chat_input.py, tests/agent_command/test_agent_command.py, tests/robot_command/test_robot_command.py |
| US1.2 | AC1.2.1–AC1.2.3 | backend/app/agent_command.py, backend/app/robot_command.py | tests/agent_command/test_agent_command_speed.py, tests/robot_command/test_robot_command_speed.py |
| US1.3 | AC1.3.1–AC1.3.3 | backend/app/agent_command.py, backend/app/robot_command.py | tests/agent_command/test_agent_command_color.py, tests/robot_command/test_robot_command_color.py |

## Plan Steps

1. Set up Python backend project structure (FastAPI, websockets, package structure)
2. Implement ChatInput module — chat input validation and forwarding to AgentCommand
3. Implement AgentCommand module — LangChain Deep Agents + OpenRouter chat-to-command translation
4. Implement RobotCommand module — Bluetooth LE command sending to Sphero Mini
5. Implement React frontend — chat window, stats panel, connection status indicator
6. Implement frontend websocket client for chat input and telemetry updates
7. Implement inline speed/color selector buttons
8. Write unit tests for all components (pytest for backend, Vitest for frontend)
9. Run full test suite and verify coverage floor (80%)
10. Verify walking skeleton end-to-end: chat → agent → Bluetooth → robot movement → stats update

## Implementation Order

1. ChatInput — receives chat input, validates, forwards to AgentCommand
2. AgentCommand — translates chat to robot commands via LangChain Deep Agents + OpenRouter
3. RobotCommand — sends robot commands to Sphero Mini via Bluetooth LE
4. WebSocket integration — connects chat input and stats panel to backend

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

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before testing robot command execution
- OpenRouter API key must be configured in `.env` before testing agent command translation
- Frontend and backend run on the same machine (localhost)
- No multi-user support (single-user desktop application)
- No cloud hosting (LAN-only per NFR1)
