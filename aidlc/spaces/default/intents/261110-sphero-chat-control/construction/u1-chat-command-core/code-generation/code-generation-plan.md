# Code Generation Plan — u1-chat-command-core

Grounded in functional design [functional-spec], requirements [requirements], unit-of-work [unit-of-work], contract design [contract-summary], NFR design [nfr-design], and tech stack decisions [tech-stack-decisions].

## Plan Summary

- Builds: chat input validation, AI agent translation service, Bluetooth LE robot command sender, FastAPI app with `/health` and the chat WebSocket, structured error logging, and the chat window/API client that supplies chat commands to the stats panel
- Touches: `backend/app/`, `tests/`, `frontend/src/components/ChatWindow.tsx`, `frontend/src/services/api.ts`, `frontend/src/App.tsx` (composition and `onSendChatCommand` wiring), `requirements.txt`
- Does **not** touch U3-owned files: `StatsPanel.tsx`, `ConnectionStatus.tsx`, `RobotStateDisplay.tsx`, `ErrorDisplay.tsx`, `LanRiskBanner.tsx`, `SpeedColorSelector.tsx`, `hooks/useRobotStateConnection.ts`, `types.ts`, `constants.ts`
- Tests: pytest + coverage.py for the Python backend (BDD scenarios, 80% line floor)

## Loop-Back Repair (attempt 2)

Triggered by Build and Test loop-back 1 (`2026-11-15T21:51:37Z`,
`construction/build-and-test/test-results.md`). The previous attempt produced
plan/summary/traceability artefacts only: no `backend/app` source, no `tests/`,
and no U1 frontend. The repair must:

1. Write the six planned backend modules: `main.py` (FastAPI app, chat
   WebSocket, `/health`, static SPA serving), `chat_input.py` (validation and
   forwarding), `agent_command.py` (LangChain Deep Agents + OpenRouter
   translation with an injectable model client), `robot_command.py` (BLE command
   sender with retry/reconnect), `config.py` (`.env` loading), `models.py`
   (Pydantic models).
2. Keep LLM and BLE at injectable boundaries so the pytest suite needs neither
   an OpenRouter key nor a robot.
3. Add the runtime dependencies to `requirements.txt` (LangChain Deep Agents and
   the OpenRouter client) alongside the existing `bleak`/`fastapi` pins.
4. Write the planned pytest suites under `tests/` with Given/When/Then
   scenarios: chat input validation, agent translation, and robot command
   execution with mocked BLE. The unit command stays
   `pytest tests/ --cov=backend/app --cov-report=term-missing`.
5. Implement the frontend slice U1 owns: `ChatWindow.tsx`,
   `services/api.ts`, and `App.tsx` composing `ChatWindow` + U3's `StatsPanel`
   and passing `onSendChatCommand` so the selector buttons are enabled.
6. Update `traceability.json` so FR1.1, FR1.2, FR2 and AC1.1.1–AC1.3.3 point at
   real implementation/test files, and NFR targets use
   `../nfr-design/<file>` paths that resolve.

## User Story Mapping

| Story | AC | Implementation Files | Test File(s) |
|-------|-----|---------------------|--------------|
| US1.1 | AC1.1.1–AC1.1.5 | backend/app/chat_input.py, backend/app/agent_command.py, backend/app/robot_command.py, backend/app/models.py | tests/chat_input/test_chat_input.py, tests/agent_command/test_agent_command.py, tests/robot_command/test_robot_command.py |
| US1.2 | AC1.2.1–AC1.2.3 | backend/app/agent_command.py, backend/app/robot_command.py | tests/agent_command/test_agent_command_speed.py, tests/robot_command/test_robot_command_speed.py |
| US1.3 | AC1.3.1–AC1.3.3 | backend/app/agent_command.py, backend/app/robot_command.py | tests/agent_command/test_agent_command_color.py, tests/robot_command/test_robot_command_color.py |

**Frontend ownership after the repair.** U1 owns `frontend/src/components/ChatWindow.tsx`,
`frontend/src/services/api.ts` and the `App.tsx` composition. U3 owns the stats
components and the WebSocket hook; U1 passes `onSendChatCommand` into
`StatsPanel` and renders chat errors through U3's `ErrorDisplay` props rather
than creating a second stats panel. No U3 component is rewritten by this unit.

## Plan Steps

1. [x] Set up the Python backend package under `backend/app/` (`__init__.py`, `config.py`, `models.py`) and add the runtime dependencies to `requirements.txt`
2. [x] Implement ChatInput module — chat input validation (non-empty, UTF-8, command pattern) and forwarding to AgentCommand
3. [x] Implement AgentCommand module — LangChain Deep Agents + OpenRouter chat-to-command translation behind an injectable model client
4. [x] Implement RobotCommand module — Bluetooth LE command sending to Sphero Mini with retry-once, backoff, and reconnect
5. [x] Implement the FastAPI app — chat WebSocket, `/health`, structured logging, error surfacing, static SPA serving from `dist/`
6. [x] Implement the U1 chat window and API client — `ChatWindow.tsx`, `services/api.ts`
7. [x] Compose `App.tsx` — render `ChatWindow` + U3's `StatsPanel`, pass `onSendChatCommand`, forward errors
8. [x] Write pytest suites under `tests/` — chat input, agent command, robot command (mocked BLE and model client), Given/When/Then scenarios
9. [x] Run `python3 -m pytest tests/ --cov=backend/app --cov-report=term-missing` and reach the 80% line floor
10. [x] Verify the u1 walking-skeleton slice (chat → agent → BLE command) with mocks; stats rendering is U2/U3's verified slice
11. [x] Update `traceability.json` — map FR1.1/FR1.2/FR2 and AC1.1.x–AC1.3.x to real files; point NFR targets at `../nfr-design/<file>`
12. [x] Refresh `code-summary.md` and `source-manifest.json` to match the files actually written

## Implementation Order

1. Config + models + dependency pins (everything else imports these)
2. ChatInput — receives chat input, validates, forwards to AgentCommand
3. AgentCommand — translates chat to robot commands via an injectable LangChain Deep Agents/OpenRouter client
4. RobotCommand — sends robot commands to Sphero Mini via Bluetooth LE, with retry and reconnect
5. FastAPI app — chat WebSocket, `/health`, structured logging, static `dist/` serving
6. ChatWindow + `services/api.ts` + `App.tsx` composition with `onSendChatCommand`
7. Pytest suites (mock BLE and the model client), then coverage run
8. Traceability, code summary and source manifest refresh

## Assumptions & Open Questions

- Sphero Mini Bluetooth LE pairing must be completed before a live robot run
- OpenRouter API key must be configured in `.env` before a live agent run; the automated suite uses an injected fake client and needs no key
- Frontend and backend run on the same machine (localhost)
- No multi-user support (single-user desktop application)
- No cloud hosting (LAN-only per NFR1)
- The repair assumes U3's stats components stay as built; U1 only wires them into `App.tsx`. If U3's replay changes their props, U1's `App.tsx` follows the U3 prop types.

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


