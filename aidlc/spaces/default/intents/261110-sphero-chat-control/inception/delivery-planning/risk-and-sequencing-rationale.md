# Risk & Sequencing Rationale — Sphero Mini Chat Control

Grounded in unit-of-work [unit-of-work], unit-of-work-dependency [unit-of-work-dependency], contract-summary [contract-summary], and team-practices [team-practices].

## Sequencing Heuristic

Walking-skeleton-first, then value-for-the-rest. No formal WSJF scoring model was selected (the user declined formal scoring at Delivery Planning Q2). Bolt order follows the dependency DAG: U1 → U2 → U3, which is serial.

## Rationale for Bolt Order

| Bolt | Unit | Reasoning | User's Worry Addressed |
|------|------|-----------|------------------------|
| Bolt 1 | U1 (u1-chat-command-core) | Walking skeleton: proves chat → robot → stats end-to-end before adding features. The user's biggest worry is Bluetooth LE pairing/connection instability on Linux (Delivery Planning Q6 = A). Building U1 first surfaces this risk immediately. | Bluetooth LE pairing/connection instability |
| Bolt 2 | U2 (u2-telemetry) | Depends on U1 (command execution status interface). Adds telemetry reception from the Sphero Mini. | AI command translation quality (validated in Bolt 1) |
| Bolt 3 | U3 (u3-stats-ui) | Depends on U2 (telemetry event format). Renders stats UI and chat UI error display. | Frontend websocket connection (de-risked by U1's chat path) |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation | Bolt Addressed |
|------|------------|--------|------------|----------------|
| Bluetooth LE pairing/connection instability on Linux | High | High | Build U1 (walking skeleton) first; pair early; document pairing steps in README.md | Bolt 1 |
| OpenRouter model producing unclear or unsafe robot commands | Medium | High | U1 error handling: unclear messages trigger rephrase; errors stop robot and show in chat UI | Bolt 1 |
| LangChain Deep Agents integration complexity | Medium | Medium | U1 uses Deep Agents directly (confirmed at feasibility Q3); validate early in Bolt 1 | Bolt 1 |
| Frontend websocket connection to Python backend | Low | Medium | U3 websocket client; U1 websocket server; contract defined in contract-design | Bolt 3 |
| OpenRouter API key not available | Low | High | User confirmed they will provide when ready; .env never committed | Bolt 1 (blocked until key provided) |

## Risk-First Argument

The user's stated top worry (Delivery Planning Q6 = A) is Bluetooth LE pairing/connection instability on Linux. Walking-skeleton-first directly addresses this: Bolt 1 exercises the Bluetooth LE command path end to end, surfacing pairing and connection issues immediately rather than late in the project. This is a risk-first argument disguised as walking-skeleton-first — both point to the same first Bolt.

## Walking Skeleton Confirmation

team.md affirms: "On — build the walking skeleton first: a thin end-to-end slice (chat → robot → stats) that proves the pieces connect before the real features go in."

Bolt 1 (U1) is the walking skeleton: chat input → AI translation → Bluetooth LE command → robot movement. It does not yet include live stats rendering (that's Bolt 3) but proves the command path end to end. U2 adds telemetry reception; U3 adds stats UI rendering. The skeleton checkpoint (human approval after Bolt 1) gates continuation to Bolt 2.

## Assumptions & Open Questions

- OpenRouter API key: user will provide when ready; blocks Bolt 1 until provided
- Sphero Mini Bluetooth LE pairing: user has Ubuntu desktop; pairing instructions in README.md
- Bolt execution is serial (DAG chain U1 → U2 → U3); parallel development possible where DAG allows but checkpoints remain serial
