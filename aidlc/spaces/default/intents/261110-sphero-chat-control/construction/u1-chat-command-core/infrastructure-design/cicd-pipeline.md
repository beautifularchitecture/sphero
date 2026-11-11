# CI/CD Pipeline — u1-chat-command-core

Grounded in NFR requirements [reliability-requirements], functional design [functional-spec], and contract design [contract-summary].

## Build Stages

| Stage | Purpose | Commands | Artifacts |
|-------|---------|----------|-----------|
| Lint | Check code style and formatting | `black --check .`, `ruff check .` | None (pass/fail) |
| Type check | Verify type correctness | `mypy .` | None (pass/fail) |
| Unit tests | Run unit tests with coverage | `pytest --cov=src --cov-report=term-missing` | Coverage report (HTML/XML) |
| Integration tests | Run integration tests (mocked Bluetooth/OpenRouter) | `pytest --cov=src --cov-report=term-missing -k "integration"` | Coverage report (HTML/XML) |

## Deployment Stages

| Stage | Purpose | Mechanism | Rollback |
|-------|---------|-----------|----------|
| Build | Build React SPA frontend | `cd frontend && npm install && npm run build` | Previous build artifacts |
| Deploy | Copy backend + frontend to Linux host | `scp -r backend/ frontend/build/ user@linux-host:/opt/sphero-chat/` | Previous deployed version (kept as previous) |
| Restart | Restart backend service | `sudo systemctl restart sphero-chat-backend` | Previous systemd service state |

## Rollback Procedures

| Failure Scenario | Rollback Action | Responsibility |
|------------------|-----------------|----------------|
| Build fails (lint/type/test) | Block deployment; developer fixes locally | Developer |
| Deploy fails (copy fails) | Restore previous deployed files from backup | Developer |
| Backend fails to start | Rollback to previous systemd service state; roll back files | Developer |
| Post-deploy smoke test fails | Roll back to previous deployed version | Developer |

## Secrets Management

| Secret | Storage | Access | Rotation |
|--------|---------|--------|----------|
| OpenRouter API key | `.env` file at project root | Loaded via environment variable at backend startup | Manual rotation; update `.env` and restart backend |
| No other secrets | N/A | N/A | N/A |

## Assumptions & Open Questions

- Single-user desktop application; no separate staging/production environments
- Deployment is manual (copy files to Linux host, restart backend service)
- No CI/CD pipeline automation; tests run locally via pytest
- OpenRouter API key provided by user and stored in `.env` (never committed)
- No containerization; backend runs directly on Linux host Python environment