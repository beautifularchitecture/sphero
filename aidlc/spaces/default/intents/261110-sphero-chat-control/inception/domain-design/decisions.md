# Architecture Decision Records — Sphero Mini Chat Control

## ADR-001: Five-component decomposition

### Context
The system needs logical building blocks for chat input, AI translation, Bluetooth command sending, telemetry reception, and stats UI rendering. The requirements analysis (FR1–FR4) and user stories (US1.1–US1.5) define these capabilities. The question was whether to use a fine-grained decomposition (five components) or a coarser one (two or three components).

### Decision
Use five components: ChatInput, AgentCommand, RobotCommand, RobotTelemetry, StatsDisplay. Each component owns a distinct business concern and its own entities. ChatInput owns ChatMessage; AgentCommand and RobotCommand share command handling; RobotTelemetry owns RobotState; StatsDisplay renders the UI.

### Consequences
- **Positive**: Clear ownership boundaries, each component has a single responsibility, changes to one component (e.g., the AI model) don't ripple to others, entities are unambiguously owned.
- **Negative**: More components means more inter-component interfaces to define and maintain in Contract Design.
- **Neutral**: Deployment topology (monolith vs. separate services) is deferred to Units Generation; this domain design only defines logical boundaries.

### Alternatives Rejected
- **Three components** (ChatInput, RobotControl, StatsUI): Would merge AgentCommand and RobotCommand into one, coupling AI translation with Bluetooth communication. Rejected because AI model changes and Bluetooth protocol changes have different change rates.
- **Two components** (Frontend, Backend): Too coarse; would conflate UI rendering with backend logic, making it harder to assign entity ownership and test components in isolation.

## ADR-002: Synchronous function-call interactions within the backend

### Context
Components ChatInput, AgentCommand, RobotCommand, and RobotTelemetry need to communicate with each other. The question was whether to use synchronous function calls or async message queues.

### Decision
Use synchronous function calls for ChatInput → AgentCommand → RobotCommand → RobotTelemetry, with an event-style publish/subscribe from RobotTelemetry → StatsDisplay for UI updates.

### Consequences
- **Positive**: Simpler to implement and reason about for an MVP on a single machine; no message queue infrastructure needed; clear request/response flow for command validation.
- **Negative**: Tighter coupling between backend components; a failure in one component blocks the caller until it recovers.
- **Neutral**: The event-style telemetry → UI path decouples the stats panel from the command pipeline, allowing the UI to update independently.

### Alternatives Rejected
- **Async message queue for all interactions**: Rejected because it adds infrastructure complexity (queue broker, message serialization, consumer management) that is unnecessary for a single-machine MVP with low message volume.

## ADR-003: RobotState owned by RobotTelemetry, not StatsDisplay

### Context
The RobotState entity (direction, orientation, color, position) represents the robot's current state. The question was whether it should be owned by RobotTelemetry (which receives it) or StatsDisplay (which renders it).

### Decision
Own RobotState in RobotTelemetry. StatsDisplay subscribes to RobotState events but does not own the entity.

### Consequences
- **Positive**: Single source of truth for robot state; StatsDisplay is a pure UI renderer with no business logic; RobotTelemetry can normalize telemetry before publishing.
- **Negative**: StatsDisplay depends on RobotTelemetry's event format; changes to the telemetry shape require updates to both components.
- **Neutral**: Entity ownership follows the principle that the component that produces the data owns it.

### Alternatives Rejected
- **RobotState owned by StatsDisplay**: Rejected because StatsDisplay is a UI component; owning domain state in a UI component mixes concerns and makes the state harder to test independently of the UI.
