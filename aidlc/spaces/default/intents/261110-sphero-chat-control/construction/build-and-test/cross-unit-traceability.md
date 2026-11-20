# Cross-Unit Traceability — sphero-chat-control

Stage: `build-and-test` (3.6) · Source: `aidlc engine sensor-traceability --stage build-and-test`
Replay run: 2026-11-19T20:22Z (UTC) · Re-entry: `Modify`

## Verdict

**PASS** — `pass: true`, `uncovered: []`. All 30 traced requirement and
acceptance IDs are covered (built or settled `N/A`-with-reason), across all three
units: `u1-chat-command-core`, `u2-telemetry` and `u3-stats-ui`.

## Sensor output summary

| Metric | Value |
|---|---|
| `pass` | `true` |
| Uncovered IDs | 0 |
| Covered IDs | 30 (FR1.1, FR1.2, FR2, FR3, FR4, NFR1–NFR8, AC1.1.1–AC1.1.5, AC1.2.1–AC1.2.3, AC1.3.1–AC1.3.3, AC1.4.1–AC1.4.2, AC1.5.1–AC1.5.4) |
| Units represented in coverage | `u1-chat-command-core`, `u2-telemetry`, `u3-stats-ui` |

## Per-ID coverage

| ID | Covered | Built in / settlement | Owning stage / Unit | Verdict |
|---|---|---|---|---|
| FR1.1 | Yes | `backend/app/chat_input.py` | code-generation / u1-chat-command-core | Covered |
| FR1.2 | Yes | `backend/app/agent_command.py` | code-generation / u1-chat-command-core | Covered |
| FR2 | Yes | `backend/app/robot_command.py` | code-generation / u1-chat-command-core | Covered |
| FR3 | Yes | `backend/app/chat_input.py` | code-generation / u1-chat-command-core | Covered |
| FR4 | Yes | `backend/app/main.py` | code-generation / u1-chat-command-core | Covered |
| NFR1 | Yes | via `u3: NFR1.2`, `NFR1.3`, `NFR1.4`, `NFR1.5` | u3-stats-ui | Covered |
| NFR2 | Yes | via `u1: NFR2.1`, `NFR2.2`; `u2: NFR2.1`–`NFR2.4` | u1-chat-command-core, u2-telemetry | Covered |
| NFR3 | Yes | via `u1: NFR3.1`–`NFR3.6`; `u3: NFR3.1`–`NFR3.5` | u1-chat-command-core, u3-stats-ui | Covered |
| NFR4 | Yes | via `u1: NFR4.1`–`NFR4.5`; `u2: NFR4.1`–`NFR4.6`; `u3: NFR4.2` | u1, u2, u3 | Covered (timing targets remain `Unverified` — see summary) |
| NFR5 | Yes | `N/A`-with-reason: no formal WCAG requirement; native button semantics and readable contrast | u3-stats-ui/code-generation | Covered (settled N/A) |
| NFR6 | Yes | `frontend/src/test-setup.ts` | u3-stats-ui | Covered |
| NFR7 | Yes | via `u1: NFR7.1`, `NFR7.2`, `NFR7.3` | u1-chat-command-core | Covered (coverage floors all Met; CI owned by ci-pipeline) |
| NFR8 | Yes | via `u1: NFR8.1` | u1-chat-command-core | Covered |
| AC1.1.1 | Yes | `tests/chat_input/test_chat_input.py` | u1-chat-command-core | Covered |
| AC1.1.2 | Yes | `tests/chat_input/test_chat_input.py` | u1-chat-command-core | Covered |
| AC1.1.3 | Yes | `tests/chat_input/test_chat_input.py` | u1-chat-command-core | Covered |
| AC1.1.4 | Yes | `tests/chat_input/test_chat_input.py` | u1-chat-command-core | Covered |
| AC1.1.5 | Yes | `tests/chat_input/test_chat_input.py` | u1-chat-command-core | Covered |
| AC1.2.1 | Yes | `tests/agent_command/test_agent_command_speed.py` | u1-chat-command-core | Covered |
| AC1.2.2 | Yes | `tests/agent_command/test_agent_command_speed.py` | u1-chat-command-core | Covered |
| AC1.2.3 | Yes | `tests/agent_command/test_agent_command_speed.py` | u1-chat-command-core | Covered |
| AC1.3.1 | Yes | `tests/agent_command/test_agent_command_color.py` | u1-chat-command-core | Covered |
| AC1.3.2 | Yes | `tests/agent_command/test_agent_command_color.py` | u1-chat-command-core | Covered |
| AC1.3.3 | Yes | `tests/agent_command/test_agent_command_color.py` | u1-chat-command-core | Covered |
| AC1.4.1 | Yes | `u2_telemetry/ble_listener.py`; `frontend/src/hooks/useRobotStateConnection.ts` | u2 + u3 | Covered |
| AC1.4.2 | Yes | `u2_telemetry/service.py`; `frontend/src/components/LanRiskBanner.tsx` | u2 + u3 | Covered |
| AC1.5.1 | Yes | `tests/integration/test_walking_skeleton.py`; `frontend/src/components/ErrorDisplay.tsx` | u1 + u3 | Covered |
| AC1.5.2 | Yes | `tests/main/test_main.py`; `frontend/src/components/ErrorDisplay.tsx` | u1 + u3 | Covered |
| AC1.5.3 | Yes | `tests/robot_command/test_robot_command.py`; `frontend/src/components/ErrorDisplay.tsx` | u1 + u3 | Covered |
| AC1.5.4 | Yes | `frontend/src/components/ChatWindow.test.tsx`; `frontend/src/components/ErrorDisplay.tsx` | u1 + u3 | Covered |

## Resolution of the first-pass findings

1. **U1 entirely untraced** — resolved: the six backend modules, `/health`, the
   chat UI and the pytest suites now exist and are traced to FR1.1, FR1.2, FR2
   and AC1.1.x–AC1.3.x.
2. **Cross-cutting NFRs unmapped** — resolved: NFR5 is settled `N/A`-with-reason
   and NFR6 is an `OK` row pointing at `frontend/src/test-setup.ts` in U3 Code
   Generation; NFR7/NFR8 trace through U1's coverage and BDD work.
3. **U1 traceability target paths wrong** — resolved: U1 rows now carry
   workspace-relative targets that the sensor resolves.
4. **U3's covered rows overstated readiness** — resolved: the relative-WebSocket
   defect (former NFR3.1 `Not Met`) is fixed with an absolute `ws://`/`wss://`
   URL and three BDD tests; the jsdom stderr is gone.

## Findings to surface at the gate

- **Browser-evidence gap.** NFR3.2–NFR3.5 (u3) are covered by jsdom tests only;
  no real browser engine ran them, so those quality targets remain `Unverified`
  in the Target Verification Matrix. This does not affect the cross-unit
  traceability pass (they are traced to real code and tests).
- **Timing/hardware gap.** NFR4.1–NFR4.4 (u1), NFR4.1–NFR4.3 (u2) and NFR2.1
  (u2) are traced to their implementations but have no wall-clock/hardware
  measurement and no performance-validation stage scheduled.
