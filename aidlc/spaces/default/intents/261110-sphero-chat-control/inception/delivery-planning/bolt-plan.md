# Bolt Plan — Sphero Mini Chat Control

Grounded in unit-of-work [unit-of-work], unit-of-work-dependency [unit-of-work-dependency], stories [stories], contract-summary [contract-summary], team-practices [team-practices], and components [components].

## Definitions

- **Bolt**: one build pass over a piece of the work, ending in something that runs. Each Bolt executes one Unit of Work through its applicable Construction stages and Code Generation, ending at a verified completion checkpoint.
- **Walking skeleton**: the first Bolt delivers the smallest working end-to-end slice — chat → robot → stats — before later Units. Its Definition of Done includes a real integrated check and human checkpoint approval.

## Sequencing Heuristic

Walking-skeleton-first, then value-for-the-rest. No formal WSJF scoring model (the user declined formal scoring). Bolt order follows the dependency DAG: U1 → U2 → U3, which is serial (each Unit depends on the previous). Parallel development is possible where the DAG allows (U2's telemetry listener can be developed alongside U1's command path; U3's UI skeleton alongside U1), but execution is serial because the DAG chain forces sequential completion.

## Bolt 1 — u1-chat-command-core (Walking Skeleton)

**Included Units of Work:** U1 (u1-chat-command-core)  
**Unit kind:** service  
**Complexity:** L  
**Stories:** US1.1, US1.2, US1.3  
**Walking skeleton marker:** Yes — this is the walking skeleton Bolt  
**Architecture proven:** chat input → AI translation (Deep Agents + OpenRouter) → Bluetooth LE command → robot movement, end to end  
**Expected demo:** User types "roll forward" in the chat UI; the Sphero Mini moves forward; stats panel shows direction/orientation/color/position (telemetry reception works; stats UI rendering comes in Bolt 3)

**Definition of Done:**
- Chat input endpoint accepts and forwards messages
- Deep Agents + OpenRouter translates chat into robot commands (forward/back/left/right/stop, speed, color)
- Bluetooth LE commands reach the Sphero Mini and the robot moves
- Error handling: unclear messages trigger rephrase; errors stop the robot and show in the chat UI
- BDD acceptance criteria US1.1–US1.3 pass
- Walking skeleton verified end to end (chat → robot motion observed)
- Human checkpoint approval obtained

**Confidence hypothesis:** Shipping this Bolt proves that chat → AI agent → Bluetooth LE → robot motion works end to end on the user's Ubuntu desktop, de-risking the two biggest unknowns (Bluetooth LE pairing stability, AI command translation quality).

**Prerequisites:**
- OpenRouter API key provided by the user (user confirmed they will provide when ready)
- Sphero Mini charged and pair-able (user confirmed Ubuntu desktop; pairing instructions in README.md)

## Bolt 2 — u2-telemetry

**Included Units of Work:** U2 (u2-telemetry)  
**Unit kind:** service  
**Complexity:** M  
**Stories:** US1.4 (telemetry reception part)  
**Walking skeleton marker:** No  
**Architecture proven:** Bluetooth LE telemetry reception → RobotState normalization → event publishing to stats UI  
**Expected demo:** Robot telemetry (direction, orientation, color, position) flows from the Sphero Mini through U2 and is available as events for U3 to consume

**Definition of Done:**
- Bluetooth LE telemetry listener receives direction, orientation, color, position from the Sphero Mini
- RobotState entity normalized and published as events
- Command execution status from U1 received and correlated
- Connection error handling and disconnection recovery
- BDD acceptance criteria US1.4 (telemetry reception part) pass
- Human checkpoint approval obtained

**Confidence hypothesis:** Shipping this Bolt proves that robot telemetry flows reliably from the Sphero Mini to the UI layer, de-risking the telemetry reception path before stats rendering.

**Prerequisites:** Bolt 1 complete (U1 command execution status interface stable)

## Bolt 3 — u3-stats-ui

**Included Units of Work:** U3 (u3-stats-ui)  
**Unit kind:** ui  
**Complexity:** M  
**Stories:** US1.4 (stats UI rendering), US1.5  
**Walking skeleton marker:** No  
**Architecture proven:** RobotState events → stats panel rendering → live observability + chat UI error display  
**Expected demo:** Stats panel shows live direction, orientation, color, position; connection status indicator; inline speed/color selector buttons; error messages shown in chat UI

**Definition of Done:**
- Stats panel subscribes to RobotState events and renders direction, orientation, color, position
- Connection status indicator (connected/disconnected/pairing/error)
- Inline speed/color selector buttons alongside chat input
- Error messages shown in chat UI for agent errors, Bluetooth permission denied, robot disconnect
- BDD acceptance criteria US1.4 (stats UI part), US1.5 pass
- Human checkpoint approval obtained

**Confidence hypothesis:** Shipping this Bolt proves that the full observability loop (chat → robot → stats → user) is complete and usable end to end.

**Prerequisites:** Bolt 2 complete (U2 telemetry event format stable)

## Bolt Sequence

| Bolt | Unit | Kind | Stories | Complexity | Walking Skeleton? | Depends On |
|------|------|------|---------|------------|-------------------|------------|
| 1 | U1 | service | US1.1, US1.2, US1.3 | L | Yes | None |
| 2 | U2 | service | US1.4 (telemetry) | M | No | Bolt 1 |
| 3 | U3 | ui | US1.4 (UI), US1.5 | M | No | Bolt 2 |

## Assumptions & Open Questions

- OpenRouter API key: user will provide when ready; stored in .env, never committed
- Bluetooth LE pairing: user has Ubuntu desktop; pairing instructions documented in README.md
- Parallel development: U2's telemetry listener and U3's UI skeleton can be developed alongside U1's command path, but execution checkpoints remain serial per the DAG
