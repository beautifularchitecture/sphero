# Performance Requirements — u3-stats-ui

Grounded in functional-spec [functional-spec], business rules [rules], requirements [requirements], contract-summary [contract-summary], unit-of-work [unit-of-work], and the nfr-requirements questions answered for this unit [nfr-requirements-questions]. The telemetry ceiling and reconnect context come from the u2-telemetry NFR answers [nfr-requirements-questions-u2].

## NFR3 — Stats Panel Refresh and Rendering

NFR3 requires the SPA stats panel to show direction, orientation, colour and position, refreshed on every robot state change. The requirements below turn that into testable targets for the U3 client, given Contract 2's fire-and-forget `/ws/robot-state` stream and U2's published ceiling of up to 10 RobotStateChanged events per second.

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR3.1 | Refresh on every event | Every RobotStateChanged event received on `/ws/robot-state` updates the panel state and is not dropped while the page is open | NFR3, BR1.5.1, Q2 |
| NFR3.2 | Event-to-render latency | No measured target: new values are shown as soon as the browser renders the caused update (no added debounce, batching, or artificial delay) | NFR3, Q1 |
| NFR3.3 | Sustained event rate | The panel handles the agreed U2 ceiling of 10 events per second by rendering each event as it arrives, with no coalescing and no throttle | Q2, u2 NFR4.2 |
| NFR3.4 | Stream recovery | When the stream drops, the client reconnects with exponential backoff of 1 s, 2 s, 4 s, 8 s, capped at 30 s, retrying for as long as the page stays open, and the current attempt is reflected in the connection indicator. **Delivery guarantee** — Contract 2's error handling declares "Event is dropped; consumer reconnects on next publish" (at-most-once, no replay). Per this assumption, gaps in the stream are accepted as lost; the panel shows the pre-drop state until the first new event after reconnect, and any stale marker clears on that first new event. The implementer should record this assumption and carry it forward rather than attempt to recover dropped events. | Q3, Contract 2 error handling, NFR3.1 |
| NFR3.5 | Stale-data display | On stream loss the last known values stay visible but are marked stale, the connection indicator shows disconnected, and the last-update timestamp stops advancing instead of being cleared. **Initial state** — when the page loads with no robot connected, the connection indicator shows disconnected and values are blank/dashed until the first event arrives; a quiet-but-open socket is treated as "connected" until the heartbeat-free connectionStatus field changes. **Reconnect** — on a successful reconnect the stale marker clears on the first new RobotStateChanged event, not on the reconnect itself. | Q4, US1.4, BR1.5.3, components.md |

## Performance Rationale

- **NFR3.1 (refresh on every event):** NFR3 and BR1.5.1 both require the panel to refresh on *every* robot state change, so the client must subscribe once and apply every delivered event for the life of the page. Nothing in the U3 design buffers events away.
- **NFR3.2 (no measured render target):** Per Q1 the person chose no measured target — values appear as soon as the browser paints them. This keeps the acceptance test behavioural ("the new value is on screen after the event is applied") instead of timing-sensitive, which suits a single-user LAN tool. It does not remove NFR3.1: the update must still happen on the event, just without a stopwatch target.
- **NFR3.3 (10 events per second, no coalescing):** Per Q2 the panel renders each event the moment it arrives rather than coalescing per animation frame. U2's agreed ceiling is 10 events per second (u2 NFR4.2), which is well inside what a React render of a handful of text fields can absorb, so the simpler "render every event" behaviour is safe and keeps the displayed state trivially consistent with the last event. Because events are not coalesced, the panel must not add its own throttle (option C was rejected).
- **NFR3.4 (reconnect with backoff):** Per Q3 the client owns reconnection, because Contract 2 is fire-and-forget and explicitly drops events for an unavailable consumer. Backoff caps at 30 s so a long outage does not turn into a reconnect storm, while retrying indefinitely keeps the page useful without a reload. The attempt count belongs on screen so the person can tell "still trying" from "connected".
- **NFR3.5 (stale, not blank):** Per Q4 the panel keeps the last known values and marks them stale rather than replacing them with dashes. Replacing values with dashes was rejected because it discards the only record of the robot's last state; freezing silently was rejected because US1.4 requires a visible disconnected status. Dashes remain reserved for fields that were missing from a delivered payload (BR1.5.3).

## Assumptions & Open Questions

- U2 sustains no more than 10 RobotStateChanged events per second, as agreed in the u2-telemetry NFR answers; if that ceiling rises, NFR3.3 is re-checked rather than assumed to hold.
- "Rendered as soon as the browser renders it" (NFR3.2) is verified behaviourally — the panel shows the value after the event is applied — not with a timing assertion in the test suite.
- The reconnect schedule (NFR3.4) assumes a single browser tab per user; several simultaneously open tabs each reconnect independently, which the LAN-only single-user deployment tolerates.
- Accessibility remains "usable, not certified" per NFR5: buttons keep native semantics and text keeps readable contrast, but no WCAG conformance target is set.
