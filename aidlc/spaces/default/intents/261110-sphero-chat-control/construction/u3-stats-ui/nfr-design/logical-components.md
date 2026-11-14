# Logical Components — u3-stats-ui

**Grounded in**: functional-spec [functional-spec], security-design [security-design], performance-design [performance-design], tech-stack-decisions [tech-stack-decisions], contract-summary [contract-summary], and unit-of-work [unit-of-work].

## Component Catalogue

| Component | In scope / owned by | Responsibility | Key Interactions & Interface | Dependencies |
|-----------|---------------------|---------------|------------------------------|--------------|
| **StatsPanel** (u3-stats-ui, in-scope) | u3-stats-ui | Top-level stats UI container: displays robot state (direction, orientation, colour, position, timestamp), last-update time, visible event counter, stale marker, and composes child controls/indicators. | Consumes hook state: `state: RobotStateView`, `connection: ConnectionView`, `reconnectAttempt: number`, `eventCount: number`, `isStale: boolean`, `lastUpdatedAt?: string`. Renders `LanRiskBanner`, `ConnectionStatus`, telemetry fields, `SpeedColorSelector`, and (when an error prop is provided) `ErrorDisplay`. Receives `onSendChatCommand?: (command: string) => void` from parent/container and passes it to `SpeedColorSelector`. | `useRobotStateConnection` hook. BR1.5.1, BR1.5.2, BR1.5.3, BR1.5.5, NFR3.1–NFR3.5, NFR1.2, NFR1.4, NFR1.5. |
| **LanRiskBanner** (u3-stats-ui, in-scope) | u3-stats-ui | Display the accepted LAN-only unauthenticated risk notice required by NFR1.4. | Rendered by `StatsPanel` at the top of the panel (above connection/status/telemetry content). **Always visible, non-dismissible**, in all connection states. Static content from in-repo constant: "LAN-only design: unauthenticated WebSocket. Anyone on this LAN can read robot telemetry and send movement commands." No props from network payloads. | NFR1.4, security-design.md. |
| **ConnectionStatus** (u3-stats-ui, in-scope) | u3-stats-ui | Show BLE/stream connection state on the stats panel. | Props: `status: "connected" | "disconnected" | "pairing" | "error" | "reconnecting"`, `reconnectAttempt?: number`, `isStale: boolean`. Displays "reconnecting (attempt N)" when applicable and disconnected/stale indicators per NFR3.4/NFR3.5. | BR1.5.2, RobotState `connectionStatus`/hook-derived state. |
| **ErrorDisplay** (u3-stats-ui, in-scope UI component) | u3-stats-ui | Render an error report surfaced to the stats UI (BR1.5.4) as escaped text. | Props: `error: { type: string; message: string; timestamp: string } | null`. When `error` is non-null, displays type, message, and timestamp; when null, renders nothing. Rendering is React-escaped only (no raw HTML). **Ownership/boundary:** u3-stats-ui owns this presentational component and its safe rendering; it does **not** own the chat transcript/surface or U1/U2 error production. The hosting UI/container (chat or page layout, potentially provided by another unit/integration layer) passes error reports into `StatsPanel`/`ErrorDisplay` when errors are relevant to the stats view. | BR1.5.4, NFR1.2, AC1.5.4 (display aspect). |
| **SpeedColorSelector** (u3-stats-ui, in-scope) | u3-stats-ui | Provide speed (low/medium/high) and color (red/blue/green) selector buttons and emit chat-command intents. | Props: `onSendChatCommand: (command: string) => void`, `disabled?: boolean`. On click emits `set speed <level>` or `set color <color>` exactly as command text. It does **not** call U1 directly and does **not** own transport. | BR1.5.5, Q4, functional-spec US1.2/US1.3. |
| **WebSocket Bridge (`useRobotStateConnection` hook)** (u3-stats-ui, in-scope) | u3-stats-ui | Manage `/ws/robot-state` connection lifecycle, reconnection, parsing/validation, and state projection for the UI. | Initiates WebSocket on mount and re-establishes on close per backoff. Parses/validates frames; applies valid events, drops malformed frames safely, tracks event count/last update/stale/reconnect attempt. Exposes typed hook result consumed by `StatsPanel`. | Contract 2, NFR3.1–NFR3.5, NFR1.2, NFR1.5, tech-stack-decisions. |
| **Chat command transport / chat surface (external dependency)** | **Consumed, not owned by u3-stats-ui** | Deliver chat command text to U1 and own the chat transcript/input surface. | u3-stats-ui depends on a container-provided callback `onSendChatCommand(command: string)` that forwards the command through the established chat input path to U1. Any broader chat UI (transcript, composer) is outside u3-stats-ui ownership unless separately assigned. | U1 command path, frontend-components/API integration, Contract 3 (indirect via U1). |

## Component Boundaries & Ownership

- Each in-scope component owns its own rendering and local view responsibilities. No component reaches into another's internal state except through explicit props/hook return values.
- **Inbound telemetry path (owned by u3-stats-ui):** WebSocket `/ws/robot-state` → `useRobotStateConnection` → `StatsPanel` → `ConnectionStatus` / telemetry fields / `LanRiskBanner` / stale & counter indicators.
- **Inbound error-display path (partially owned):** error reports are produced by U1/U2 (out of scope for u3-stats-ui production) and delivered to u3-stats-ui via an explicit `error` prop/input; u3-stats-ui owns safe rendering in `ErrorDisplay` but not the chat transcript surface.
- **Outbound command path (intent owned, transport consumed):** `SpeedColorSelector` emits command text via `onSendChatCommand` callback → hosting container/chat command transport (external to u3-stats-ui) → U1. This is a separate outbound path and must not be described as telemetry flowing "to" `SpeedColorSelector`.
- `ChatUI`/chat transcript ownership is not assumed inside u3-stats-ui; integration provides the command-forwarding callback and, where applicable, the surface that hosts error/chat content.

## Interaction Patterns

### Robot State Update (inbound)

1. U2 publishes `RobotStateChanged` on `/ws/robot-state` (Contract 2, at-most-once/no replay assumed).
2. `useRobotStateConnection` receives frames via native `WebSocket`, initiated on mount and re-established on reconnect.
3. Hook parses/validates each frame: valid events update state, increment event count, and set last-updated timestamp; malformed/non-JSON/shape-mismatched frames are dropped, logged as non-payload `console.error`, and leave prior valid state/stale/timestamp unchanged.
4. `StatsPanel` renders `LanRiskBanner` (always visible), `ConnectionStatus`, telemetry values (dash for missing/null), stale marker, and event counter.
5. Stale marker clears only on the first new valid event after reconnect (not on socket open).

### Chat Command Forwarding (outbound, transport consumed)

1. User clicks a speed (low/medium/high) or color (red/blue/green) control in `SpeedColorSelector`.
2. `SpeedColorSelector` invokes `props.onSendChatCommand("set speed <level>")` or `props.onSendChatCommand("set color <color>")`.
3. The hosting container/external chat command transport forwards the command through the established chat input path to U1.
4. U1 translates and executes the command (Contract 3 / U1 responsibility). u3-stats-ui does not perform translation or direct U1 network calls except through the provided callback contract.

### Error Display (inbound display, production external)

1. U1 or U2 produces an error (unrecognized message, backend error, Bluetooth error, disconnect) outside u3-stats-ui.
2. The hosting/integration layer passes the error report to `StatsPanel` as `error={{ type, message, timestamp }}` when it should be shown in the stats context.
3. `ErrorDisplay` renders the escaped error type, message, and timestamp (BR1.5.4, NFR1.2).
4. On disconnect-related errors affecting movement display, `StatsPanel` reflects disconnected/error state and stale/indicator behavior per NFR3.5 and AC1.5.4 display expectations; command execution/robot stop behavior remains owned by U1/U2.