# Tech Stack Decisions — u3-stats-ui

Grounded in functional-spec [functional-spec], business rules [rules], requirements [requirements], contract-summary [contract-summary], unit-of-work [unit-of-work], and the nfr-requirements questions answered for this unit [nfr-requirements-questions]. The frontend stack already fixed for this project is carried forward from the u1-chat-command-core NFR requirements [tech-stack-decisions-u1] and is not re-decided here.

## Frontend Framework and Build

| Decision | Choice | Justification | Source |
|----------|--------|---------------|--------|
| Framework | React | Project frontend framework, already fixed for the SPA in U1 | tech-stack-decisions-u1 |
| Language | TypeScript | Type-safe component and WebSocket payload handling | tech-stack-decisions-u1 |
| Build tool | Vite | Project build and dev server; serves the SPA that U1 embeds as static files | tech-stack-decisions-u1, unit-of-work |
| Component structure | StatsPanel, ConnectionStatus, ErrorMessage, SpeedColorSelector | Component split agreed in the functional design of this unit | functional-spec |

## Telemetry Client

| Decision | Choice | Justification | Source |
|----------|--------|---------------|--------|
| WebSocket client | Native browser `WebSocket` API | One endpoint (`/ws/robot-state`), no fallback transports, no extra runtime dependency | Contract 2, Q3 |
| Reconnect strategy | In-house exponential backoff (1 s, 2 s, 4 s, 8 s, capped at 30 s) in a typed hook | Backoff window and attempt display agreed in Q3; a retry library would add a dependency for one schedule | NFR3.4, Q3 |
| Event handling | Apply every event on arrival, no coalescing layer | Q2 chose render-every-event over per-frame coalescing; U2's ceiling is 10 events/sec (u2 NFR4.2) | NFR3.3, Q2 |
| Client state | React local state plus a small context for the socket | Single-page, single-user UI; a global state library is unjustified | Q2, Q3 |
| Payload contract | TypeScript types mirroring the Contract 2 RobotState shape, optional fields included | Keeps BR1.5.3's dash-for-missing behaviour type-checked at the boundary | Contract 2, BR1.5.3 |

## Styling

| Decision | Choice | Justification | Source |
|----------|--------|---------------|--------|
| Styling | Tailwind CSS utility classes | Person's choice in Q6 over CSS Modules, a global stylesheet, or a component library | Q6 |
| Design-system dependency | None (no MUI, Chakra, or similar) | Tailwind covers layout and the small component set without a runtime component library | Q6 |
| Accessibility posture | Native buttons, labels, and semantic HTML; readable contrast; no WCAG certification | NFR5 asks for a usable UI, not a certified one | NFR5 |

## Testing and Quality Gates

| Decision | Choice | Justification | Source |
|----------|--------|---------------|--------|
| Test runner | Vitest + React Testing Library | Frontend test stack already fixed for the project | NFR6, tech-stack-decisions-u1 |
| Test methodology | BDD: Given/When/Then scenarios first, then implement, then run | Team practice recorded for this intent | NFR8 |
| Coverage floor | 80% line coverage, not weakenable to make a step pass | Scope floor for this intent | NFR7 |
| CI | Frontend tests and type-check run before merge; failure blocks merge | Team practice for this intent | NFR7 |
| Lint and format | Project-level linter and formatter config in the repo root | Project code-style rule | team.md |

## Client-Side Logging and Diagnostics

| Decision | Choice | Justification | Source |
|----------|--------|---------------|--------|
| On-screen diagnostics | Connection indicator, last-updated timestamp, and a visible event counter on the panel | Q7 option B: the UI is the person's only live window into the robot, so a counter makes "receiving but unchanged" visible | Q7 |
| Client logging | `console.error` for socket failures only; no telemetry payload logging | Q7 option A baseline; keeps robot data out of the console and matches U2's errors-and-connection-changes-only logging | Q7, u2 Q4 |
| Analytics / telemetry from the UI | None | LAN-only, single-user tool; no third-party calls | NFR1, C-03 |

## Tech Stack Rationale

- **Carried-forward frontend stack:** React, TypeScript, and Vite are already the project's SPA stack and Vitest + React Testing Library its test stack (NFR6, u1 tech-stack-decisions). U3 adds no alternative framework, bundler, or test runner; the decisions above only fill in what U3 itself needs.
- **Native WebSocket over a socket library:** Contract 2 defines one server-to-consumer endpoint with no authentication and no fallback transport (NFR1.4, Q5). The browser's built-in `WebSocket` covers it, and the reconnect loop in NFR3.4 is a few lines in a typed hook, so a socket library would be a dependency without a job.
- **Tailwind CSS:** Q6 selected utility classes. It fits the small component set (panel, indicator, error block, selector buttons) and avoids a runtime component library, while keeping the markup accessible through native elements per NFR5. It is a build-time dependency of the Vite pipeline, not a runtime service.
- **Render-every-event:** Q2 chose rendering each event over per-frame coalescing. At U2's agreed ceiling of 10 events per second the straightforward subscription is sufficient, and removing the coalescing layer also removes a source of "the screen disagrees with the last event" bugs. NFR3.1 and NFR3.3 carry the requirement.
- **Visible event counter and minimal logging:** Q7 option B adds a counter or debug line to the panel and limits client logging to socket failures. U2 logs only errors and connection changes, so the UI is the live window; the counter distinguishes a quiet robot from a dead stream without printing telemetry payloads into the console.
- **Static serving:** unit-of-work places the SPA inside U1's FastAPI deployment as static files, so the build must remain a plain Vite bundle with no separate frontend server. That constraint is why the stack adds no server-side rendering, no Node runtime, and no frontend secret (NFR1.3).

## Assumptions & Open Questions

- Tailwind CSS is added as a Vite build-time dependency; if the project later standardises on a different styling system, Q6 is the decision to revisit.
- The event counter required by Q7 is a count of received events shown in the panel; it is not a metrics endpoint, and nothing is shipped off the machine.
- The 80% coverage floor applies to the U3 frontend modules and is enforced in CI alongside the backend suite (NFR7).
- No frontend accessibility certification is attempted (NFR5); native controls and readable contrast are the accepted bar.
- NFR1.1: This unit (u3-stats-ui, kind `ui`) continues NFR1.x from the inception scope; NFR1.1 belongs to the U1 backend scope and is not re-declared here. The gap is intentional and noted for cross-unit traceability.
- Body text contrast: a measurable target of body text at least 4.5:1 against its background is recommended; if the team cannot commit to a measurable threshold, it is recorded as explicitly untested so the person is not approving an unverifiable target.
