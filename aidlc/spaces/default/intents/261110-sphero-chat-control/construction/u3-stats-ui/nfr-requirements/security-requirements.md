# Security Requirements — u3-stats-ui

Grounded in functional-spec [functional-spec], business rules [rules], requirements [requirements], contract-summary [contract-summary], and the nfr-requirements questions answered for this unit [nfr-requirements-questions]. The LAN-only deployment context comes from the scope document [scope-document] and NFR1; the telemetry payload shape comes from Contract 2 in contract-summary.

## NFR1 — Frontend Handling of Telemetry and Errors

NFR1 restricts the whole system to the local network with no outside access. The U3 client is the only place where telemetry and error text reach a browser, so the security posture is defined here. Per Q5 the person chose the plain posture — render everything as escaped text, keep no secrets in the frontend bundle, and leave the LAN WebSocket unauthenticated — and explicitly rejected both a client-side value whitelist and a shared token in the handshake.

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR1.2 | Safe rendering of telemetry and errors | Every value from RobotState (direction, orientation, colour, position, timestamp, connectionStatus) and every error message is rendered as React-escaped text; no `dangerouslySetInnerHTML` and no raw HTML injection path into the panel or chat error area | Q5, Contract 2, BR1.5.4 |
| NFR1.3 | No secrets in the frontend | The SPA bundle and sources contain no API keys, tokens, or OpenRouter credentials; U3 never calls OpenRouter directly and the `OPENROUTER_API_KEY` stays in U1's `.env` | Q5, C-04, Contract 3 |
| NFR1.4 | Unauthenticated LAN WebSocket | The `/ws/robot-state` connection carries no token or credential in this single-user LAN deployment; the absence of handshake authentication is a documented, accepted risk. **Scope** — this risk covers both inbound telemetry and outbound chat command paths: U3 attaches no credential when sending chat commands to U1 (frontend-components.md, API Integration Points: "Chat input to U1"), and the accepted-risk statement has been widened to note that anyone able to reach the LAN endpoint can read robot telemetry and send commands that move the robot. | Q5, NFR1, C-03, frontend-components.md |
| NFR1.5 | Missing-field fallback | Only fields absent from a delivered RobotState payload render as a dash; fields with an explicit `null` value also render as a dash, aligning NFR1.5 with BR1.5.3's trigger of "missing or null attributes" (rules.md, BR1.5.3). This avoids the contradiction where a payload carrying a `null` direction would display as literal text while the business rule requires a dash. | Q5, BR1.5.3 |

## Security Rationale

- **NFR1.2 (escaped rendering):** The panel renders values that originate from Bluetooth telemetry and from backend error reports — untrusted input from the browser's point of view. Rendering through React's default escaping, with no HTML-injection escape hatch, removes the script-injection path while leaving the display faithful. Error messages sit in the chat UI beside user content and get the same treatment.
- **NFR1.3 (no frontend secrets):** The only credential in the system is the OpenRouter API key, and C-04 already confines it to `.env` on the backend. U3 talks to U1 over the LAN; it has no reason to hold a key, so the frontend bundle stays credential-free. This also keeps the built `dist/` safe to serve as static files from U1's FastAPI app.
- **NFR1.4 (no handshake token):** Per Q5 the WebSocket stays unauthenticated. On a single-user LAN with no outside access (NFR1, C-03) the token would protect nothing the network boundary does not already protect, and it would add a handshake step to every reconnect in NFR3.4. The consequence is recorded, not hidden: anyone able to reach the LAN endpoint can read robot telemetry. Revisiting this is the trigger if the app is ever exposed beyond the LAN.
- **NFR1.5 (dash for missing, text for present):** Q5 rejected a value whitelist (option B), so the panel does not second-guess delivered values. BR1.5.3 still governs gaps: a field the payload omits shows a dash. The rule keeps "no whitelist" from turning into "render `undefined`", and it keeps the safety property in NFR1.2 — values are displayed as inert text.

## Assumptions & Open Questions

- The SPA is served from U1's backend on the same LAN host and is never exposed through a public ingress; if that changes, NFR1.4's accepted risk no longer holds and handshake authentication is reconsidered.
- Sphero telemetry and backend error strings are treated as untrusted display text even though the source is the person's own robot; escaped rendering (NFR1.2) makes this assumption cheap to keep.
- No content security policy, CORS tightening, or rate limiting is added for this LAN-only MVP; those would be follow-ups if the deployment boundary widens.
- The rejected options (client-side whitelist, shared handshake token) are recorded here so a later reviewer does not re-open them as omissions.
