# Security Design — u3-stats-ui

**Grounded in**: security-requirements [security-requirements], functional-spec [functional-spec], contract-summary [contract-summary], tech-stack-decisions [tech-stack-decisions], and nfr-requirements questions [nfr-requirements-questions].

## NFR1 — Frontend Handling of Telemetry and Errors

### Approach: Plain LAN posture (per Q5 choice)

Per Q5 the person explicitly chose the plain posture: render everything as escaped text, keep no secrets in the frontend bundle, and leave the LAN WebSocket unauthenticated. Both a client-side value whitelist and a shared token in the handshake were rejected.

| Requirement | Design Decision | Implementation Note |
|-------------|-----------------|---------------------|
| **NFR1.2** Safe rendering of telemetry and errors | Render every value from `RobotState` (direction, orientation, colour, position, timestamp, connectionStatus) and every error message as React-escaped text; use no `dangerouslySetInnerHTML` and no raw HTML injection path | React's default escaping removes the script-injection path while leaving the display faithful. Error reports surfaced in u3-stats-ui's `ErrorDisplay` component get the same escaping treatment. Malformed/non-JSON or schema-mismatched WebSocket payloads are never rendered: they are dropped, logged via `console.error` with non-payload diagnostics, and do not mutate displayed telemetry state. |
| **NFR1.3** No secrets in the frontend | The SPA bundle and sources contain no API keys, tokens, or OpenRouter credentials; `OPENROUTER_API_KEY` stays in U1's `.env`; U3 never calls OpenRouter directly | The only credential in the system is the OpenRouter API key, confined to `.env` on the backend (C-04). U3 talks to U1 over the LAN and has no reason to hold a key. The built `dist/` is safe to serve as static files from U1's FastAPI app. CI enforces this with a deterministic bundle scan (see Technical Approach). |
| **NFR1.4** Unauthenticated LAN WebSocket | The `/ws/robot-state` connection carries no token or credential in this single-user LAN deployment; the absence of handshake authentication is a documented, accepted risk | **Scope**: this risk covers both inbound telemetry and outbound chat command paths. U3 attaches no credential when sending chat commands to U1. The accepted-risk statement is widened to note that anyone able to reach the LAN endpoint can read robot telemetry and send commands that move the robot. The risk is communicated by an always-visible `LanRiskBanner` in `StatsPanel` (see Technical Approach and Logical Components). Documented risk — not hidden. |
| **NFR1.5** Missing-field fallback | Fields absent from a delivered `RobotState` payload render as a dash; fields with an explicit `null` value also render as a dash, aligning with BR1.5.3's trigger of "missing or null attributes" | Avoids the contradiction where a payload carrying a `null` direction would display as literal text while the business rule requires a dash. Keeps "no whitelist" from turning into "render `undefined`", and keeps the safety property in NFR1.2 — values are displayed as inert text. |

### Assumptions & Open Questions

- **LAN-only boundary**: The SPA is served from U1's backend on the same LAN host and is never exposed through a public ingress; if that changes, NFR1.4's accepted risk no longer holds and handshake authentication is reconsidered.
- **Untrusted display text**: Sphero telemetry and backend error strings are treated as untrusted display text even though the source is the person's own robot; escaped rendering (NFR1.2) makes this assumption cheap to keep.
- **No CSP/CORS/rate limiting**: No content security policy, CORS tightening, or rate limiting is added for this LAN-only MVP; those would be follow-ups if the deployment boundary widens.
- **Rejected options**: The client-side value whitelist and shared handshake token are recorded here so a later reviewer does not re-open them as omissions.
- **Observability**: Security event observability is limited to the UI banners and CI bundle-inspection checks; no separate security telemetry or audit logging is emitted from this LAN-only MVP.

### Technical Approach

The security posture is enforced at the component and CI levels:

1. **Safe rendering and payload handling** — no `dangerouslySetInnerHTML` anywhere in u3-stats-ui components (`StatsPanel`, `ConnectionStatus`, `ErrorDisplay`, `LanRiskBanner`, `SpeedColorSelector`). All telemetry and error strings are rendered as React-escaped text. WebSocket `onmessage` parsing/validation is wrapped in `try/catch`; malformed/non-JSON or schema-mismatched payloads are dropped, logged as `console.error` with a non-payload diagnostic, and never rendered or applied to state.
2. **Deterministic bundle secret scan (NFR1.3, CI gate)** — after `vite build`, CI runs a scan over text assets in `dist/` (`**/*.{js,mjs,cjs,css,html,map,json,txt}`), excluding binary assets, using a fixed pattern set:
   - exact env/key identifiers: `OPENROUTER_API_KEY`, `VITE_OPENROUTER_API_KEY`
   - credential assignment patterns: `(?i)(api[_-]?key|authorization|bearer)\s*[:=]\s*['\"][^'\"]{8,}['\"]`
   The command fails (non-zero, blocks merge) on any match and prints the matching file path and line number; no matched secret value is echoed in full in CI logs beyond the bounded match context required for remediation. Expected tooling: `rg`/`grep -RInE` (or equivalent) invoked by the CI script `scripts/check-dist-secrets.sh` (or package script alias). Violations are remediated by removing the secret from frontend source/config, rotating it if exposed, and rebuilding. Generic words like `token`/`credential` alone are not matched to avoid false positives.
3. **LanRiskBanner (NFR1.4, required UI control)** — `LanRiskBanner` is an explicit, always-visible, non-dismissible banner rendered at the top of `StatsPanel` (above connection/status/telemetry content) in every connection state (disconnected, connecting/reconnecting, connected, pairing, error, stale). Content is static, sourced from in-repo UI copy constant (not from network payloads): **"LAN-only design: unauthenticated WebSocket. Anyone on this LAN can read robot telemetry and send movement commands."** It remains visible for the lifetime of the page and is removed only if deployment boundary widens beyond LAN (a future design change), at which point NFR1.4 is reconsidered. Placement, visibility, and content are verifiable in component/unit tests.
4. **Null/missing-field handling (NFR1.5)** — in the `RobotState` renderer, a field present with value `null` or absent from the payload is rendered as a dash (`-`), consistent with BR1.5.3. Non-string/non-expected types are treated as invalid payloads per the parse/validation rule above and not partially rendered.