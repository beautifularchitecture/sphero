# Contract Design — Questions

## Sources

- [unit-of-work] — units-generation/unit-of-work.md
- [unit-of-work-dependency] — units-generation/unit-of-work-dependency.md
- [components] — domain-design/components.md
- [requirements] — requirements-analysis/requirements.md

## Unit Context

Three units from Units Generation:
- U1 (u1-chat-command-core) — service: chat input, AI translation via OpenRouter, Bluetooth LE command sending
- U2 (u2-telemetry) — service: Bluetooth LE telemetry reception, RobotState event publishing
- U3 (u3-stats-ui) — ui: stats panel rendering, inline speed/color selectors

Dependency DAG: U1 → U2 → U3

Inter-unit boundaries (candidate contracts):
1. U1 → U2: command execution status (sync callback)
2. U2 → U3: RobotState telemetry events (publish/subscribe)

External boundary:
3. U1 → OpenRouter API: chat-to-command translation via LangChain Deep Agents (third-party API, public/external)

## Q1. [Product] Public/external API surface — Which units expose an API consumed outside the system?

U1 exposes the chat input via websockets to the SPA frontend (U3). U3 is the SPA frontend that users interact with externally.

- A. U1 exposes a websocket API consumed externally (by U3's React SPA); U3 consumes it — this is the public/external API boundary
- B. U1 exposes a REST API consumed externally
- C. No external API boundary — all communication is internal between units
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. U1 exposes a websocket API consumed externally (by U3's React SPA); U3 consumes it — this is the public/external API boundary

## Q2. [Product] Integration mechanism per boundary — How do units communicate across each boundary?

- A. U1 → U2: sync callback (function call); U2 → U3: event (publish/subscribe); U1 → OpenRouter: sync REST/HTTP
- B. U1 → U2: async message queue; U2 → U3: async message queue; U1 → OpenRouter: sync REST/HTTP
- C. U1 → U2: sync REST/HTTP; U2 → U3: sync REST/HTTP; U1 → OpenRouter: sync REST/HTTP
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. U1 → U2: sync callback (function call); U2 → U3: event (publish/subscribe); U1 → OpenRouter: sync REST/HTTP

## Q3. [Product] Contract ownership — Which unit owns each contract spec?

- A. U1 owns the U1→U2 contract; U2 owns the U2→U3 contract; U1 owns the U1→OpenRouter contract (provider owns each)
- B. The consumer of each boundary owns the contract spec
- C. A separate contract spec is owned by a shared "contracts" unit/library
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. U1 owns the U1→U2 contract; U2 owns the U2→U3 contract; U1 owns the U1→OpenRouter contract (provider owns each)

## Q4. [Product] Versioning and breaking-change policy — How are contract changes managed?

- A. Semantic versioning on each contract spec; breaking changes require consumer agreement; additive changes are safe (consumers ignore unknown fields)
- B. No formal versioning; breaking changes communicated informally
- C. Contracts versioned per-release; breaking changes bundled with releases
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. Semantic versioning on each contract spec; breaking changes require consumer agreement; additive changes are safe (consumers ignore unknown fields)

## Q5. [Product] Error, timeout, and retry behaviour at each boundary — What happens when things go wrong?

- A. U1 → U2: sync callback returns error; U2 retries once with backoff; U2 → U3: event delivery is fire-and-forget (no retry); U1 → OpenRouter: 3 retries with exponential backoff, then error to chat UI
- B. All boundaries: 3 retries with fixed delay, then fail fast with error message
- C. U1 → U2: fail fast, no retry; U2 → U3: fire-and-forget; U1 → OpenRouter: 5 retries with fixed delay
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. U1 → U2: sync callback returns error; U2 retries once with backoff; U2 → U3: event delivery is fire-and-forget (no retry); U1 → OpenRouter: 3 retries with exponential backoff, then error to chat UI
