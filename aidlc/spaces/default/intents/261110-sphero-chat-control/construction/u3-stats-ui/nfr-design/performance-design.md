# Performance Design — u3-stats-ui

**Grounded in**: performance-requirements [performance-requirements], tech-stack-decisions [tech-stack-decisions], functional-spec [functional-spec], contract-summary [contract-summary], and nfr-requirements questions [nfr-requirements-questions].

## NFR3 — Stats Panel Refresh and Rendering

### Approach: Render-every-event subscription

The StatsDisplay component subscribes to the `/ws/robot-state` WebSocket endpoint (Contract 2) and applies every delivered event immediately. No buffering, no coalescing per animation frame, and no artificial delay.

| Requirement | Design Decision | Implementation Note |
|-------------|-----------------|---------------------|
| **NFR3.1** Refresh on every event | Subscribe for the life of the page and apply every delivered valid `RobotStateChanged` event | The WebSocket subscription is **initiated once on component mount** (`useEffect` with empty dependency list). When the socket closes, the hook **re-establishes a new socket** according to the NFR3.4 backoff schedule; each socket instance uses the same `onmessage`/`onclose`/`onerror` handling semantics. Every valid delivered event is applied immediately (no event queue or buffer). |
| **NFR3.2** Event-to-render latency | No measured target; values appear as soon as the browser paints them | Verified behaviourally: "the new value is on screen after the event is applied". The update happens in the same tick as valid event processing — no `setTimeout`, no `requestAnimationFrame` batching. This suits a single-user LAN tool and avoids timing-sensitive tests. |
| **NFR3.3** Sustained event rate (10 events/sec) | Render each event as it arrives; no coalescing, no throttle | U2's agreed ceiling is 10 events/sec (u2 NFR4.2). A straightforward subscription at this rate is well inside what a React render of a handful of text fields can absorb. React's normal render batching/reconciliation ensures only changed fields update. The rejected option (per-frame coalescing) is documented as an omission. |
| **NFR3.4** Stream recovery — exponential backoff | Client-owned reconnection with visible attempt counter | On stream loss (`onclose` or terminal `onerror` leading to close), the hook initiates exponential backoff: 1s → 2s → 4s → 8s, capped at 30s, retrying for as long as the page stays open. The attempt count is reflected in the connection indicator (`reconnecting (attempt N)`). After a successful reconnect, the stale marker clears on the **first new valid `RobotStateChanged` event**, not on the reconnect/open itself. Malformed frames are ignored and do not break reconnect logic. |
| **NFR3.5** Stale-data display | Last known values marked stale; connection indicator shows disconnected | On stream loss: (1) last known values stay visible with a "stale" badge, (2) connection indicator shows "disconnected", (3) last-update timestamp stops advancing. When the page loads with no robot connected: connection indicator shows "disconnected" and values are blank/dashed until the first valid event arrives. A quiet-but-open socket is treated as "connected" until the heartbeat-free `connectionStatus` field changes in a received valid event. Invalid/malformed frames do not clear stale state and do not advance the last-update timestamp. |

### Assumptions & Open Questions

- **U2 ceiling**: Sustained rate of 10 RobotStateChanged events per second; if that ceiling rises, NFR3.3 is re-checked rather than assumed to hold.
- **Behavioural verification**: "Rendered as soon as the browser renders it" is verified behaviourally — the panel shows the value after the event is applied — not with a timing assertion in the test suite.
- **Multiple tabs**: The reconnect schedule assumes a single browser tab per user; several simultaneously open tabs each reconnect independently, which the LAN-only single-user deployment tolerates.
- **Accessibility**: Remains "usable, not certified" per NFR5: buttons keep native semantics and text keeps readable contrast, but no WCAG conformance target is set.
- **Scalability**: This unit is designed for single-user LAN deployment; scalability beyond one concurrent user is not addressed here (follow-up if deployment boundary widens).
- **Reliability**: The fire-and-forget WebSocket model (Contract 2) accepts that events may be dropped for unavailable consumers; reconnection logic (NFR3.4) recovers from transient losses but does not guarantee delivery of previously dropped events.
- **Observability**: The visible event counter (Q7) and connection indicator provide operational insight into stream health; no server-side metrics or telemetry are emitted from this unit.

### Technical Approach

The reconnection logic is implemented in a typed hook `useRobotStateConnection()` that:

1. **Initiates** a subscription to `/ws/robot-state` on mount via the browser's native `WebSocket` API, and **re-establishes** a new socket on each reconnect according to NFR3.4.
2. On `onclose` (and on terminal socket errors), triggers exponential backoff with a visible attempt count while preserving the last known panel state as stale per NFR3.5.
3. On `onmessage`, parses the frame as JSON and validates the expected `RobotState` shape (object with required `timestamp: string`; other Contract 2 fields optional as specified). A **valid** event is applied to React state immediately and increments the visible event counter. A **malformed/non-JSON/shape-mismatched** frame is dropped: it is logged via `console.error` with a non-payload diagnostic (e.g. "Dropped malformed RobotState frame"), does not update state, does not increment the event counter, does not clear stale state, and does not advance the last-update timestamp. Message-handling errors are caught so they do not break the active socket or reconnect logic.
4. On successful reconnect, clears the stale marker on the **first new valid** `RobotStateChanged` event (not on socket open).

The visible event counter (from Q7) counts only valid received events and is shown in the panel to distinguish a quiet robot from a dead stream without printing telemetry payloads into the console. Socket failures are logged via `console.error` with non-payload diagnostics only.