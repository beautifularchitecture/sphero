# Monitoring Design — u3-stats-ui

**Grounded in**: nfr-design (performance-design, security-design, logical-components) [nfr-design], functional-spec [functional-spec], tech-stack-decisions [tech-stack-decisions-u3], contract-summary [contract-summary].

## Scope

u3-stats-ui is a browser-side SPA with no server-side runtime infrastructure of its own. Monitoring is implemented as in-UI indicators and client-side diagnostics (no centralized metrics/logs/traces backend provisioned for this unit). This design realizes the UI-relevant observability, performance, security, and reliability decisions from NFR design for a LAN-only MVP.

## Metrics & KPIs

| Metric | Source | Threshold / Target | Why it matters |
|--------|--------|---------------------|----------------|
| Valid telemetry events received (event counter) | `useRobotStateConnection` hook (counts only valid parsed events) | Increments on each valid `RobotStateChanged`; expected up to 10 events/sec per NFR3.3/u2 ceiling | Distinguishes a quiet robot from a dead stream; confirms live updates without logging payloads (Q7). |
| Last update timestamp | UI state updated on first processing of each valid event | Advances on every valid event; stops advancing on stream loss/stale (NFR3.5) | Shows freshness of displayed robot state. |
| Connection/reconnect state | Hook + `ConnectionStatus` component | States: `connected`, `reconnecting (attempt N)`, `disconnected`, `pairing`, `error` as applicable; backoff 1s/2s/4s/8s capped at 30s (NFR3.4) | Makes stream health and recovery attempts visible to the operator. |
| Stale indicator | `StatsPanel` derived state | Set on stream loss; cleared only on first new valid event after reconnect (not on socket open) (NFR3.5) | Prevents misreading frozen last-known values as live. |
| Dropped malformed frames | `onmessage` parse/validation path | Any non-JSON/shape-mismatched frame dropped (count not surfaced in MVP UI unless added later) | Protects safe rendering and recovery; diagnosable via console errors. |

## Alerts

| Alert | Condition | Severity | Routes to |
|-------|-----------|----------|-----------|
| Stream disconnected / stale (UI indicator) | WebSocket close/terminal error or no valid updates after loss; stale marker shown and last-update stops | Warning (operator-visible) | On-screen `ConnectionStatus` + stale badge in `StatsPanel` (LAN single user) |
| Reconnecting with attempt count (UI indicator) | Reconnect in progress per backoff schedule | Info (operator-visible) | On-screen `ConnectionStatus` text `reconnecting (attempt N)` |
| Socket failure diagnostic | `onerror`/`onclose` or message-handling exception | Error (diagnostic) | Browser `console.error` with non-payload message only (no telemetry payload logging) |
| Malformed telemetry frame dropped | JSON parse failure or schema mismatch in `onmessage` | Error (diagnostic) | Browser `console.error` with non-payload diagnostic (e.g. "Dropped malformed RobotState frame"); no UI crash |
| CI bundle secret scan failure | Match for forbidden secret/key patterns in built `dist/` assets | Blocking (CI) | CI job failure with file path/line context; merge blocked until remediated |

## SLIs / SLOs

| SLI | SLO target | Measurement window |
|-----|------------|--------------------|
| Valid event application correctness | Every valid delivered `RobotStateChanged` updates panel state and increments event counter (NFR3.1) | Per session / behavioural verification in tests and manual LAN runs |
| Reconnect behavior under stream loss | Client retries with 1s,2s,4s,8s capped at 30s while page open; stale clears on first new valid event (NFR3.4/NFR3.5) | Per disconnect/reconnect episode (behavioural) |
| Safe rendering of untrusted data | No raw HTML injection; malformed payloads never rendered/applied (NFR1.2) | Per event/frame; enforced by component tests and code review |
| Frontend secret hygiene | No `OPENROUTER_API_KEY` / `VITE_OPENROUTER_API_KEY` or credential assignment leaks in `dist/` per scan rules (NFR1.3) | Per CI build of frontend bundle |

No numeric availability/latency SLOs are defined for this LAN-only UI unit beyond behavioural targets above; render latency has no measured target per NFR3.2.

## Logs & Tracing

| Concern | Design | Notes |
|---------|--------|-------|
| Client logging | `console.error` only for socket failures and dropped malformed frames, with non-payload diagnostics | No telemetry payload logging; aligns with Q7 and NFR1.2/NFR3.4 resilience. |
| Log aggregation | None (browser-local console) | LAN single-user MVP; no centralized log shipping. |
| Distributed tracing | None for u3-stats-ui | No backend trace propagation owned by this unit; WebSocket is fire-and-forget Contract 2. |
| Dashboards | The stats panel itself is the operator dashboard | Includes `LanRiskBanner`, `ConnectionStatus`, telemetry fields, last-updated, stale marker, and event counter. |

## Assumptions & Open Questions

- Observability remains UI/console-local for MVP; if deployment expands, add structured client telemetry/error reporting with privacy controls (no secrets/payloads) as a follow-up.
- Event counter reflects valid received events only; malformed frames are intentionally excluded from count/state advancement.