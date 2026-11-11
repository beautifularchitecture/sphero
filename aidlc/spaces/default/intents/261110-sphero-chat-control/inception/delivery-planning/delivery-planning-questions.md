# Delivery Planning — Questions

## Sources

- [unit-of-work] — units-generation/unit-of-work.md
- [unit-of-work-dependency] — units-generation/unit-of-work-dependency.md
- [components] — domain-design/components.md
- [decisions] — domain-design/decisions.md
- [requirements] — requirements-analysis/requirements.md
- [stories] — user-stories/stories.md
- [mockups] — refined-mockups/mockups.md
- [contract-summary] — contract-design/contract-summary.md
- [team-practices] — practices-discovery/team-practices.md

## Unit Context

Three units from Units Generation:
- U1 (u1-chat-command-core) — service — chat input, AI translation via OpenRouter, Bluetooth LE command sending — stories US1.1, US1.2, US1.3 — Complexity: L
- U2 (u2-telemetry) — service — Bluetooth LE telemetry reception, RobotState event publishing — story US1.4 — Complexity: M
- U3 (u3-stats-ui) — ui — stats panel rendering, inline speed/color selectors — stories US1.4, US1.5 — Complexity: M

Dependency DAG: U1 → U2 → U3 (serial chain — each unit depends on the previous)

Walking skeleton is ON (affirmed at practices-discovery): the first Bolt must be a thin end-to-end slice proving the pieces connect before real features go in.

## Strategic Questions

### Q1. [Product] What should we build first?

Options for the Bolt sequencing heuristic:

- A. Walking-skeleton-first: U1 (chat → robot end-to-end) as Bolt 1, then U2 + U3 as later Bolts — proves the whole thing hangs together before adding features
- B. Value-first: ship the most valuable capability first (stats observability US1.4), then movement, then color/speed
- C. Risk-first: Bluetooth LE connection risk first, then AI translation, then UI
- D. Mix: walking skeleton first (U1), then value-first for remaining units (U2 stats telemetry, U3 stats UI)
- E. Not yet defined
- X. Other (please specify)

[Answer]:

### Q2. [Product] Should we score and rank the work with a formal model (WSJF-style)?

This decides whether to use Weighted Shortest Job First scoring (value + urgency + risk reduction) ÷ size, or a simpler heuristic.

- A. Yes — use WSJF-style scoring; weight risk heavily since Bluetooth LE + AI are the unknowns
- B. Yes — use WSJF-style scoring; weight value heavily since this is a learning project
- C. No — no formal scoring model; use walking-skeleton-first then value-for-the-rest
- D. Not yet defined
- X. Other (please specify)

[Answer]:

### Q3. [Product] How big should one Bolt be?

- A. Single Unit per Bolt: Bolt 1 = U1, Bolt 2 = U2, Bolt 3 = U3 (three Bolts, one Unit each)
- B. Bundle related Units: Bolt 1 = U1 + U2 (backend services), Bolt 2 = U3 (frontend UI)
- C. Thin cross-Unit slices: Bolt 1 = walking skeleton (U1 end-to-end), Bolt 2 = U2 + U3 together (telemetry + stats UI)
- D. Not yet defined
- X. Other (please specify)

[Answer]:

### Q4. [Product] Can several Bolts be built at the same time?

- A. Serial only — the DAG chain U1 → U2 → U3 means each Bolt depends on the previous; build one after another
- B. Parallel where possible — U2's telemetry listener can be developed alongside U1's command path; U3's UI skeleton alongside U1
- C. Not yet defined
- X. Other (please specify)

[Answer]:

### Q5. [Product] External dependencies that could hold us up

- A. OpenRouter API key (.env) — user must provide before U1 can build the AI translation
- B. Sphero Mini Bluetooth LE pairing — user must have the robot charged and pair-able before U1's walking skeleton
- C. Neither — both are already available
- D. Not yet defined
- X. Other (please specify)

[Answer]:

### Q6. [Product] What worries you most about this build?

This helps decide which Bolt to ship first to surface the biggest unknown.

- A. Bluetooth LE pairing/connection instability on Linux
- B. OpenRouter model producing unclear or unsafe robot commands
- C. LangChain Deep Agents package integration complexity
- D. Frontend websocket connection to the Python backend
- E. None / not sure
- X. Other (please specify)

[Answer]:
