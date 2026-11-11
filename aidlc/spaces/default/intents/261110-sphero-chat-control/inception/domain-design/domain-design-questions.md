# Domain Design — Questions

## Sources

- [requirements] — requirements-analysis/requirements.md
- [stories] — user-stories/stories.md
- [team-practices] — practices-discovery/team-practices.md

## Q1. [Product] Component boundaries — What are the distinct logical building blocks?

Each component owns its business logic, entities, and lifecycle. Databases, caches, queues, and third-party services are external dependencies, not components.

- A. Five components: ChatInput (chat → agent), AgentCommand (chat → robot commands), RobotCommand (commands → robot via Bluetooth), RobotTelemetry (telemetry → UI), StatsDisplay (stats panel UI)
- B. Three components: ChatInput (chat + agent), RobotControl (commands + telemetry), StatsUI (stats panel)
- C. Two components: Frontend (chat + stats UI), Backend (agent + Bluetooth robot control)
- D. Not yet defined — I'll decide during design
- X. Other (please specify)

[Answer]: A. Five components: ChatInput (chat → agent), AgentCommand (chat → robot commands), RobotCommand (commands → robot via Bluetooth), RobotTelemetry (telemetry → UI), StatsDisplay (stats panel UI)

## Q2. [Product] Entity ownership — Which component owns each entity?

Every entity has exactly one owning component. Ambiguous ownership is a design smell.

- A. ChatMessage owned by ChatInput; RobotCommand owned by RobotCommand; RobotState (direction/orientation/color/position) owned by RobotTelemetry
- B. ChatMessage owned by ChatInput; RobotCommand owned by AgentCommand; RobotState owned by RobotCommand
- C. ChatMessage owned by ChatInput; RobotCommand owned by RobotCommand; RobotState owned by StatsDisplay (UI)
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. ChatMessage owned by ChatInput; RobotCommand owned by RobotCommand; RobotState (direction/orientation/color/position) owned by RobotTelemetry

## Q3. [Product] Component interactions — How do components call each other?

Specify the interaction style for each component dependency.

- A. ChatInput → AgentCommand (sync, function call); AgentCommand → RobotCommand (sync, function call); RobotCommand → RobotTelemetry (sync, callback); RobotTelemetry → StatsDisplay (event, publish telemetry)
- B. ChatInput → AgentCommand (async, message queue); AgentCommand → RobotCommand (async, message queue); RobotCommand → RobotTelemetry (async, message queue); RobotTelemetry → StatsDisplay (event, publish telemetry)
- C. ChatInput → AgentCommand (sync, function call); AgentCommand → RobotCommand (sync, function call); RobotCommand → StatsDisplay (sync, direct UI update); no RobotTelemetry component
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. ChatInput → AgentCommand (sync, function call); AgentCommand → RobotCommand (sync, function call); RobotCommand → RobotTelemetry (sync, callback); RobotTelemetry → StatsDisplay (event, publish telemetry)

## Q4. [Product] External dependencies — What infra/third-party services does each component use?

These are not components but dependencies OF components.

- A. ChatInput: none; AgentCommand: OpenRouter API (third-party-api); RobotCommand: Sphero Mini Bluetooth LE (third-party-api); RobotTelemetry: Sphero Mini Bluetooth LE (third-party-api); StatsDisplay: none
- B. ChatInput: none; AgentCommand: none; RobotCommand: OpenRouter API + Sphero Mini Bluetooth LE; RobotTelemetry: none; StatsDisplay: none
- C. ChatInput: websocket server; AgentCommand: OpenRouter API; RobotCommand: Bluetooth LE adapter; RobotTelemetry: Bluetooth LE adapter; StatsDisplay: none
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. ChatInput: none; AgentCommand: OpenRouter API (third-party-api); RobotCommand: Sphero Mini Bluetooth LE (third-party-api); RobotTelemetry: Sphero Mini Bluetooth LE (third-party-api); StatsDisplay: none

## Q5. [Product] UI component structure — How is the frontend UI decomposed?

The SPA has a chat window and stats panel. How should UI components be structured?

- A. Two UI components: ChatWindow (message input + list) and StatsPanel (direction/orientation/color/position + connection status)
- B. One UI component: MainControlScreen (chat + stats combined)
- C. Four UI components: ChatInput, MessageList, StatsPanel, ConnectionStatus
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. Two UI components: ChatWindow (message input + list) and StatsPanel (direction/orientation/color/position + connection status)
