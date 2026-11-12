# CI/CD Pipeline — u2-telemetry

Grounded in infrastructure-specification [infrastructure-specification], NFR requirements [observability-requirements, reliability-design], and team practices (continuous deployment to production on every merge).

## Pipeline Stages

The pipeline runs on every commit to `main` (team practice: continuous deployment to production on every merge). Stages are sequential:

1. **Lint** — ESLint/Ruff on Python source; fail fast on formatting and static analysis violations (< 30s).
2. **Build** — Resolve Python dependencies, compile if needed; cache aggressively (< 2 min).
3. **Unit Test** — pytest + coverage.py full suite; fail on any failure; 80% line coverage floor per NFR7 (< 3 min).
4. **SAST** — Static security scan; block on high/critical findings (< 5 min).
5. **Package** — Build deployment artifact; tag with commit SHA.
6. **Deploy Staging** — Automated; mirrors production topology at reduced scale.
7. **E2E Test** — Critical paths only (BLE telemetry reception → RobotStateChanged publish → U3 StatsDisplay update); flaky tests quarantined (< 15 min).
8. **Security Scan** — DAST against staging; dependency vulnerability check.
9. **Deploy Production** — Automated with rolling deployment (stateless service, backward-compatible changes).
10. **Smoke Test** — Verify core endpoints respond correctly post-deploy (< 2 min).
11. **Monitor** — Confirm CloudWatch metrics and alerts are active post-deploy.

## Stage → Gate Mapping

| Stage | Gate | Result |
|-------|------|--------|
| Lint | Pass/fail | Blocks build on failure |
| Build | Pass/fail | Blocks test on failure |
| Unit Test | Pass/fail + coverage ≥ 80% | Blocks package on failure |
| SAST | Pass/fail (high/critical) | Blocks deploy staging on failure |
| Deploy Staging | Automated | Blocks E2E test on failure |
| E2E Test | Pass/fail | Blocks security scan on failure |
| Security Scan | Pass/fail | Blocks deploy production on failure |
| Deploy Production | Rolling | Blocks smoke test on failure |
| Smoke Test | Pass/fail | Blocks monitor on failure |

## Deployment Strategy

**Rolling deployment** — U2 is a stateless Python service with no persistent state; instances are replaced incrementally. No blue-green (single host, double cost unjustified for MVP) and no canary (single consumer U3, low traffic). Rollback: revert the commit and re-run the pipeline; systemd auto-restarts the previous version.

## Rollback Procedures

- **Failed deploy:** `git revert <bad-commit>` and re-run the pipeline; systemd picks up the reverted code on restart.
- **Post-deploy issue:** Roll forward with a fix commit; continuous deployment re-deploys automatically.
- **Database/schema rollback:** Not applicable — no persistent data store.

## Secrets Management

- **U2:** No secrets used (NFR2.2 — no API keys, tokens, or secrets). No `.env` or secret file needed.
- **U1 (OpenRouter API key):** Loaded from `.env` at startup (OPENROUTER_API_KEY); never committed to version control (team rule: NEVER commit `.env` or `.*` files); never logged or shown in UI (Contract 3). U1 manages its own secret; U2 does not touch it.
- **CI/CD:** No secrets injected for U2 builds (nothing to deploy beyond Python source). U1's CI handles its own `.env` injection separately.

## Assumptions & Open Questions

None.
