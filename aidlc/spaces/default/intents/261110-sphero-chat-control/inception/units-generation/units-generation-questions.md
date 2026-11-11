# Units Generation — Questions

## Sources

- [components] — domain-design/components.md
- [decisions] — domain-design/decisions.md
- [requirements] — requirements-analysis/requirements.md
- [stories] — user-stories/stories.md

## Component Context

Five components from Domain Design:
- ChatInput — chat UI input, owns ChatMessage
- AgentCommand — AI translation via Deep Agents + OpenRouter
- RobotCommand — Bluetooth LE command sending to Sphero Mini
- RobotTelemetry — Bluetooth LE telemetry reception, owns RobotState
- StatsDisplay — stats panel UI rendering

Walking skeleton is ON (affirmed at practices-discovery Q2): the first Unit must be the smallest working integrated slice — chat → robot → stats end-to-end — before later Units.

## Q1. [Product] Unit boundary strategy — How should components be grouped into Units?

- A. One walking-skeleton Unit (all 5 components) + one enhancement Unit (speed/color UI buttons)
- B. One Unit per component (5 Units: ChatInput, AgentCommand, RobotCommand, RobotTelemetry, StatsDisplay)
- C. Two Units by layer: Backend Unit (AgentCommand + RobotCommand + RobotTelemetry) + Frontend Unit (ChatInput + StatsDisplay)
- D. Not yet defined — I'll decide during design
- X. Other (please specify)

[Answer]:

## Q2. [Product] Unit granularity — Coarse vs fine-grained?

- A. Coarse: 2 Units (walking skeleton + enhancements)
- B. Fine: 5 Units (one per component)
- C. Medium: 3 Units (chat/command core, telemetry, stats UI)
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q3. [Product] Dependency ordering — Should independent Units be built in parallel?

- A. Yes — Units with no dependency between them can be built simultaneously in their own project copies
- B. No — build Units one at a time in strict topological order
- C. Not yet defined
- X. Other (please specify)

[Answer]:

## Q4. [Product] Unit kinds — What kind is each Unit?

- A. Walking-skeleton Unit: `service` (deployed executable with chat + robot + stats); Enhancement Unit: `ui` (frontend buttons only)
- B. All Units: `service`
- C. Walking-skeleton Unit: `service`; Enhancement Unit: `library` (reusable UI components)
- D. Not yet defined
- X. Other (please specify)

[Answer]:

## Q5. [Product] Deployment model — How are Units deployed?

- A. Monolithic deploy (all Units deployed together as one application)
- B. Independent deploy (each Unit deployed separately)
- C. Hybrid (backend Units together, frontend Unit separate)
- D. Not yet defined
- X. Other (please specify)

[Answer]:
