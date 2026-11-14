# Infrastructure Specification — u3-stats-ui

**Grounded in**: nfr-design (performance-design, security-design, logical-components) [nfr-design], domain-design components [components], functional-spec [functional-spec], contract-summary [contract-summary], tech-stack-decisions [tech-stack-decisions-u3].

## Context

u3-stats-ui is the SPA frontend unit (React + TypeScript + Vite + Tailwind CSS) providing the stats panel, connection/status indicators, LAN risk banner, error display, and speed/color selectors. It runs in the user's browser on the same LAN as the backend, consumes robot state via WebSocket `ws/robot-state` (Contract 2, U2 → U3), and forwards chat-command intents through the hosting/chat transport to U1. No cloud resources, containers, or separate frontend runtime are required for this MVP; the built SPA is served as static files from U1's FastAPI backend.

## Deployment

| Facet | Choice | Rationale |
|-------|--------|-----------|
| Compute model | Browser-executed SPA (static assets served by U1 FastAPI) | u3-stats-ui is a client-side UI unit; no dedicated frontend server/container/VM. U1 owns HTTP serving in LAN deployment (unit-of-work/tech-stack-decisions). |
| Networking topology | LAN-only HTTP(S-optional for local MVP) + WebSocket on same LAN host/network; ingress limited to local network clients; egress limited to backend endpoints on LAN | NFR1/C-03: single-user LAN tool, no outside access. Telemetry inbound via `/ws/robot-state`; command intents outbound via U1 chat path. No public ingress, CDN, or multi-region networking. |
| Storage strategy | No persistent infrastructure storage for u3-stats-ui | UI keeps last known state in browser memory only (stale/last-updated/event count per NFR3.5). No databases, caches, or object stores owned by this unit. |
| Environments | `dev` (local developer machine/browser), `ci` (ephemeral test/build), `lan` (single-user local deployment served by U1) | Parity by build artifacts and config, not topology scale. Staging/production cloud environments are out of scope for LAN-only MVP; if boundary widens, NFR1.4 and deployment are reconsidered. |
| IaC approach | None for u3-stats-ui runtime infrastructure; repo-managed build config (Vite/Tailwind/TS) and CI workflow definitions treated as code | No provisioned cloud resources to manage via CDK/Terraform/CloudFormation. Future cloud/static hosting would introduce IaC at that point. |
| Resource sizing | Static bundle size budget guided by Vite defaults; browser runtime memory/CPU bounded by 10 events/sec render-every-event design (NFR3.3) | No server-side sizing. Design favors simple React renders and no coalescing/throttle libraries; performance validated behaviourally per NFR3.2/NFR3.3. |

## Infrastructure Services

| Service | Role | Configuration | Notes |
|---------|------|---------------|-------|
| U1 FastAPI static file hosting | Web/static asset delivery (external to u3-stats-ui, integration dependency) | Serve Vite `dist/` assets over LAN HTTP; route SPA entry as configured by U1 integration | u3-stats-ui produces static assets only; hosting/runtime is U1 responsibility. |
| U2 WebSocket endpoint `/ws/robot-state` | Telemetry event source (external provider, Contract 2) | Browser `WebSocket` client; at-most-once/no-replay assumed; reconnect/backoff handled client-side (NFR3.4) | No queue/broker/cache provisioned by u3-stats-ui. |
| Browser runtime | UI execution environment | Modern evergreen browser with WebSocket and ES module support (project baseline aligned with Vite/React/TS toolchain) | No server-side rendering or Node runtime in deployment. |
| CI runner (ephemeral) | Build/test/scan execution | Installs frontend deps, runs lint/type-check/tests/build, runs deterministic dist secret scan (NFR1.3) | Stateless; no persistent infra owned by unit. |

## Shared Infrastructure

No shared infrastructure resources are provisioned or owned by u3-stats-ui. Shared deployment surfaces (U1 static hosting, LAN network, U2 telemetry endpoint, chat command transport) are owned by other units/integration layers and consumed through explicit contracts/callbacks.

## Design Notes

- **LAN-only security posture**: unauthenticated WebSocket accepted for MVP (NFR1.4) with always-visible `LanRiskBanner`; if exposed beyond LAN, add authentication/ingress controls and revisit deployment.
- **No secrets in frontend**: `OPENROUTER_API_KEY` remains in U1 `.env`; bundle scan in CI enforces NFR1.3.
- **Reliability/observability in UI**: reconnect, stale indicators, event counter, and `console.error` diagnostics (non-payload) provide operator visibility without backend metrics infrastructure in this unit.