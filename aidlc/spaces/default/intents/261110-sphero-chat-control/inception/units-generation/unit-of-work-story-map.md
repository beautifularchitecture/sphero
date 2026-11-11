# Unit Story Map — Sphero Mini Chat Control

Grounded in user stories [stories] and requirements [requirements].

## Story-to-Unit Mapping

| Upstream ID | Unit ID | Directory | Acceptance Criteria Implemented | Source |
|-------------|---------|-----------|---------------------------------|--------|
| US1.1 | U1 | u1-chat-command-core | AC1.1.1–AC1.1.5 | [US1.1] |
| US1.2 | U1 | u1-chat-command-core | AC1.2.1–AC1.2.3 | [US1.2] |
| US1.3 | U1 | u1-chat-command-core | AC1.3.1–AC1.3.3 | [US1.3] |
| US1.4 | U2, U3 | u2-telemetry, u3-stats-ui | AC1.4.1 (U2 telemetry), AC1.4.2 (U3 UI) | [US1.4] |
| US1.5 | U1, U3 | u1-chat-command-core, u3-stats-ui | AC1.5.1–AC1.5.4 (error handling across U1 command path and U3 UI error display) | [US1.5] |

## Rows Spanning Multiple Units

| Upstream ID | Units | Split Rationale |
|-------------|-------|-----------------|
| US1.4 | U2, U3 | U2 receives and normalizes telemetry; U3 renders it on the stats panel UI |
| US1.5 | U1, U3 | U1 stops the robot and reports errors on the command path; U3 displays error messages in the chat UI |

## Implementation Order Within Each Unit

### U1 — u1-chat-command-core
1. Chat input endpoint and message validation (US1.1, AC1.1.1)
2. AgentCommand translation with Deep Agents + OpenRouter (US1.1, AC1.1.1)
3. Bluetooth LE command sending to Sphero Mini (US1.1, AC1.1.2–AC1.1.5)
4. Speed control commands (US1.2, AC1.2.1–AC1.2.3)
5. LED color commands (US1.3, AC1.3.1–AC1.3.3)
6. Error handling: unclear message rephrase, robot stop on error (US1.5, AC1.5.1–AC1.5.4 partial)
7. Walking skeleton verification: chat → robot end-to-end

### U2 — u2-telemetry
1. Bluetooth LE telemetry listener (US1.4, AC1.4.1)
2. RobotState normalization (US1.4, AC1.4.1)
3. Event publishing to stats UI (US1.4, AC1.4.1)
4. Connection error handling (US1.4, AC1.4.2 partial)

### U3 — u3-stats-ui
1. Stats panel UI skeleton (US1.4, AC1.4.2)
2. Subscribe to telemetry events and render values (US1.4, AC1.4.1)
3. Connection status indicator (US1.4, AC1.4.2)
4. Inline speed/color selector buttons (US1.2, US1.3 support)
5. Error message display in chat UI (US1.5, AC1.5.2–AC1.5.4 partial)

## Coverage Verification

| Upstream ID | Assigned | Unit Rows | Traceable |
|-------------|----------|-----------|-----------|
| US1.1 | Yes | U1 | Yes |
| US1.2 | Yes | U1 | Yes |
| US1.3 | Yes | U1 | Yes |
| US1.4 | Yes | U2, U3 | Yes |
| US1.5 | Yes | U1, U3 | Yes |

Every enumerated ID is assigned to at least one Unit; every Unit has rows in this map.

## Assumptions & Open Questions

None.
