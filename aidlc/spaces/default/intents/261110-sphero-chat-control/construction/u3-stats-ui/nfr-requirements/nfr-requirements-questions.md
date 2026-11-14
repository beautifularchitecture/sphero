# NFR Requirements Questions — u3-stats-ui

Grounded in functional-spec [functional-spec], requirements [requirements], contract-summary [contract-summary], and the telemetry NFR answers already recorded for u2-telemetry [nfr-requirements-questions].

## Q1. [Frontend] Stats panel update latency

The stats panel is supposed to refresh on every robot state change (NFR3), and U2 can publish up to 10 events per second. What budget should the UI meet between an event arriving on the WebSocket and the new values being visible on screen?

- A. Visible within 100 ms of arrival (one animation frame plus a React render at 60 Hz)
- B. Visible within 250 ms of arrival
- C. Visible within 1 second of arrival
- D. No measured target; update as soon as the browser renders it
- X. Other (please specify)

[Answer]: D

## Q2. [Frontend] Telemetry burst handling

U2's agreed ceiling is up to 10 RobotStateChanged events per second. How should the panel behave when events arrive faster than the screen refreshes?

- A. Coalesce: at most one panel update per animation frame (~16 ms), always showing the latest state
- B. Render every event the moment it arrives, with no coalescing
- C. Throttle to a fixed 2 updates per second
- D. Not yet defined
- X. Other (please specify)

[Answer]: B

## Q3. [Frontend] WebSocket reconnection when telemetry drops

Contract 2 is fire-and-forget: when U2's `/ws/robot-state` stream drops, the consumer reconnects on the next publish. What should the stats UI client do?

- A. Reconnect automatically with exponential backoff (1 s, 2 s, 4 s, 8 s, capped at 30 s), retrying for as long as the page is open, with the attempt reflected in the connection indicator
- B. Reconnect up to 3 times, then require the user to reload the page
- C. No automatic reconnection; the user reloads the page manually
- D. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q4. [Frontend] What the panel shows when telemetry stops

US1.4 requires a disconnected status when no robot is connected, and partial telemetry must render as dashes (BR1.5.3). What should happen to values already on screen when the stream stops?

- A. Keep the last known values visible but visibly stale, with the connection indicator showing disconnected and the last-update timestamp unchanged
- B. Replace every value with dashes as soon as the connection drops
- C. Freeze the panel silently with no stale or disconnected marker
- D. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q5. [Security] Frontend handling of telemetry data

The system is LAN-only with a single user and no authentication (NFR1), and every value on the panel arrives from U2 over Contract 2. What security posture should the stats UI take?

- A. Render everything as React-escaped text (no raw HTML injection), keep no secrets in the frontend bundle, and leave the LAN WebSocket unauthenticated
- B. Option A plus a client-side whitelist: only known values for direction, color, and connection status are displayed, anything else shows a dash
- C. Option A plus a shared token in the WebSocket handshake
- D. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q6. [Frontend] Styling approach for the stats panel and controls

React + TypeScript + Vite and Vitest + React Testing Library are already fixed for the frontend. How should the stats panel, connection indicator, error display, and speed/colour buttons be styled?

- A. CSS Modules: one stylesheet per component, no extra runtime dependency
- B. A single global stylesheet for the whole SPA
- C. Tailwind CSS utility classes
- D. A component library such as MUI or Chakra
- X. Other (please specify)

[Answer]: C

## Q7. [Observability] What the stats UI surfaces and logs

U2 logs only errors and connection-state changes, so the UI is the user's only live window into the robot. What should the stats UI itself surface and log?

- A. Connection indicator plus a last-updated timestamp on the panel, and client-side console errors for socket failures only, with no telemetry payload logging
- B. Option A plus a visible event counter or debug line in the panel
- C. No client-side logging at all; rely on the visible status only
- D. Not yet defined
- X. Other (please specify)

[Answer]: B
