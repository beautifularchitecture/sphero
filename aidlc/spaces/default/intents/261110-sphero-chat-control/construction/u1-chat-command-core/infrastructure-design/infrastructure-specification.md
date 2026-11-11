# Infrastructure Specification — u1-chat-command-core

Grounded in NFR requirements [nfr-requirements], functional design [functional-spec], domain design [components.md], contract design [contract-summary], and tech stack decisions [tech-stack-decisions].

## Deployment

| Facet | Choice | Rationale |
|-------|--------|-----------|
| Compute model | Single Linux machine (local) | Single-user desktop application; no cloud hosting required per NFR1 (LAN-only access) |
| Deployment topology | Single host, single instance | One user, one robot, one backend instance; no multi-tenancy or independent scaling needed |
| Networking | localhost + LAN | Backend listens on localhost (127.0.0.1) for SPA frontend; SPA served by FastAPI on same host; Bluetooth LE connects directly to Sphero Mini |
| Environments | dev = prod | Single-user desktop application; no separate staging/production environments needed |
| IaC approach | None (manual setup) | Single-user project; infrastructure is the developer's Linux machine; no cloud provisioning needed |

## Infrastructure Services

| Service | Role | Configuration | Notes |
|---------|------|---------------|-------|
| Linux OS | Host OS | Ubuntu Desktop | Provides Bluetooth LE stack (BlueZ), Python runtime, and web server |
| FastAPI Backend | Web API server | Python 3.11, uvicorn, listens on localhost:8000 | Serves React SPA frontend, exposes chat websocket endpoint, drives Bluetooth LE commands |
| React SPA | Frontend UI | React, TypeScript, Vitest | Served as static files by FastAPI; connects to backend websocket for chat input and stats display |
| Bluetooth LE | Robot communication | BlueZ, bleak/pygatt | Direct Bluetooth LE connection to Sphero Mini; pairing once at setup |

## Shared Infrastructure

| Shared Resource | Owner Unit | Consumer Units | Access Boundary |
|-----------------|------------|----------------|-----------------|
| Sphero Mini Bluetooth LE adapter | u1-chat-command-core | u1-chat-command-core | Exclusive; only RobotCommand component accesses Bluetooth LE adapter |
| Linux host machine | u1-chat-command-core | u1-chat-command-core | Exclusive; single-user desktop application |

## Assumptions & Open Questions

- Backend runs on the user's Linux desktop machine
- Sphero Mini Bluetooth LE adapter is available and paired on the Linux host
- No cloud infrastructure required (LAN-only operation per NFR1)
- No CI/CD infrastructure; manual deployment on the Linux host