# Infrastructure Specification — u2-telemetry

Grounded in NFR design [performance-design, security-design, scalability-design, reliability-design, observability-design, logical-components], functional-spec [functional-spec], contract-summary [contract-summary], domain-design [components], and infrastructure-design questions [infrastructure-design-questions].

## Deployment

| Facet | Choice | Rationale |
|-------|--------|-----------|
| Compute model | Linux host process (Python 3.14 + bleak + FastAPI) on a single Linux backend with Bluetooth | U2 receives BLE telemetry directly from the Sphero Mini; a single host with a BLE radio is the minimal deployment for the single-robot MVP (NFR4.4). No containers, no serverless — BLE requires direct hardware access. |
| Networking topology | Host network, outbound HTTPS only (Contract 3: U1→OpenRouter via U1) | U2 initiates no inbound connections. BLE is local radio. U1→U2 is a sync callback on the same host. U2→U3 is local event publish. No VPC, no load balancer needed for the MVP. |
| Storage strategy | Ephemeral in-memory only (RobotState, publish queue) | No persistent data store (NFR2.2: no secrets; telemetry is fire-and-forget per Contract 2). RobotState lives in memory for the process lifetime. |
| Environments | dev, staging, production on the same host topology | Team practice: continuous deployment to production on every merge. Staging mirrors production at reduced scale; for the MVP all three run on equivalent Linux hosts with Bluetooth. |
| IaC approach | Shell/provisioning script (no CDK/Terraform for the MVP) | Single host, single BLE radio — no cloud infrastructure to define. The robot backend is provisioned as a Linux host with BlueZ + Python. |
| Resource sizing | Single vCPU, 512 MB RAM | Telemetry at ≤10 events/sec (NFR4.2) is trivial load; BLE reception is I/O-bound, not compute-bound. |

## Infrastructure Services

| Service | Role | Configuration | Notes |
|---------|------|---------------|-------|
| Linux host (backend) | Compute host for U2 Python/bleak/FastAPI service | BlueZ stack, Python 3.14, systemd unit | Provides the BLE radio interface; U2 runs as a systemd service with auto-restart |
| bleak (Python BLE library) | BLE GATT client for telemetry reception | Async scan + connect + notifications | Receives RobotStateChanged-triggering telemetry from the Sphero Mini |
| FastAPI + WebSocket | Real-time telemetry streaming to U3 StatsDisplay | WebSocket endpoint on `robot.state.changed` | Serves Contract 2 event delivery (fire-and-forget) to the local frontend |
| Publish queue (asyncio.Queue) | In-memory buffer between BLE receive and publish | Bounded queue, single consumer coroutine | Implements Q2=A: async publish keeps BLE reception non-blocking |
| systemd | Process supervision | `Restart=always`, `RestartSec=5` | Auto-restarts U2 on crash; aligns with NFR2.3 reconnection behavior |
| OpenRouter API (via U1) | External chat-to-command translation | HTTPS, Bearer token from U1's .env | U1 owns this dependency (Contract 3); U2 does not call it directly |

## Shared Infrastructure

Not applicable — u2-telemetry is a single unit with no shared resources across units. The BLE radio and Linux host are dedicated to U2.

## Assumptions & Open Questions

None.
