# CI/CD Pipeline — u3-stats-ui

**Grounded in**: tech-stack-decisions [tech-stack-decisions-u3], security-design [security-design], nfr-design [nfr-design], team practices [team.md], and unit-of-work context [unit-of-work].

## Scope

This pipeline covers the frontend unit `u3-stats-ui` (React + TypeScript + Vite + Tailwind CSS, Vitest + React Testing Library). Build artifacts are static files (`dist/`) intended to be served by U1's FastAPI backend in a LAN-only deployment. There is no separate frontend production environment, container registry, or cloud deployment stage owned by this unit.

## Pipeline Stages and Gates

| Stage | Purpose | Key Commands / Checks | Gate / Exit Criteria |
|-------|---------|------------------------|----------------------|
| 1. Checkout & install | Reproducible dependency setup | Checkout commit; install with lockfile (e.g. `npm ci` / `pnpm install --frozen-lockfile` as project-standard) | Clean install succeeds; lockfile consistent |
| 2. Lint & format check | Code style and static hygiene | Project-configured linter/formatter checks (repo-root config) | No lint/format violations; failure blocks merge |
| 3. Type check | TypeScript correctness | `tsc --noEmit` (or project alias) | No type errors |
| 4. Unit/component tests (BDD-aligned) | Validate behaviour and acceptance scenarios | `vitest` (React Testing Library); scenarios written Given/When/Then per team posture, including reconnect/stale/malformed-payload/safe-render/banner cases | All tests pass; failure blocks merge |
| 5. Coverage | Enforce quality floor | Coverage report via Vitest/coverage tool; threshold 80% line coverage for U3 frontend modules (NFR7, additive scope floor) | >= 80% line coverage; threshold not weakenable to pass |
| 6. Build | Produce deployable static bundle | `vite build` → `dist/` | Build succeeds; artifacts produced for scan/integration |
| 7. Bundle secret scan (security gate) | Enforce NFR1.3 (no frontend secrets) | Run deterministic scan over `dist/**/*.{js,mjs,cjs,css,html,map,json,txt}` for `OPENROUTER_API_KEY`, `VITE_OPENROUTER_API_KEY`, and credential assignment patterns `(?i)(api[_-]?key|authorization|bearer)\s*[:=]\s*['\"][^'\"]{8,}['\"]` (e.g. `scripts/check-dist-secrets.sh` using `rg`/`grep -RInE`); fail on match with file/line context, do not echo full secret | No matches; failure blocks merge/deploy artifact use |
| 8. Integration/package handoff | Make bundle consumable by U1 | Publish or copy `dist/` as build artifact for U1 static-serving integration (repo/workflow-specific mechanism) | Artifact available and traceable to commit SHA |
| 9. LAN deployment verification (manual/integration context) | Confirm SPA served and connects on LAN | Served from U1 FastAPI on LAN host; verify UI loads, `LanRiskBanner` visible, WebSocket connects to `/ws/robot-state`, reconnect/stale indicators behave per NFR3 | Operator/integration confirmation for MVP (no automated public smoke environment) |

## Test Automation Integration

- **Methodology**: BDD (Given/When/Then scenarios first, then implement, then run) per team `memory/team.md`.
- **Runner/stack**: Vitest + React Testing Library (carried forward, NFR6).
- **Coverage floor**: 80% line coverage for U3 frontend modules, enforced in CI and not weakened to make steps pass.
- **Required behavioural coverage (minimum focus)**: render-every-event updates, reconnect backoff/attempt visibility, stale marker lifecycle, malformed/non-JSON frame handling, escaped rendering/no `dangerouslySetInnerHTML`, missing/null dash rendering, always-visible `LanRiskBanner`, and command callback emission for speed/color selectors.
- CI executes frontend tests/type-check before merge; failures block merge.

## Deployment Strategy

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Strategy | **Static artifact replace** (served by U1) on merge to LAN deployment context; no blue-green/canary/rolling for browser SPA unit alone | Single-user LAN MVP with static bundle delivery; version switch occurs when U1 serves updated `dist/` assets. |
| Promotion | `dev` (local) → `ci` (validated build/test/scan) → `lan` integration served by U1 | Matches MVP environment model; no cloud staging/prod promotion owned by u3-stats-ui. |
| Rollback | Re-deploy previous commit's `dist/` artifact via U1 (or `git revert` + rebuild) | Fast recovery without data migration; browser refresh loads prior bundle. |
| Feature flags | None required for MVP | Small unit and LAN-only scope; add flags later if incremental UI rollout needed. |

## Secrets Management in CI/CD

| Secret / Concern | Handling | Notes |
|------------------|----------|-------|
| `OPENROUTER_API_KEY` | **Never** stored in frontend source, build args, or CI vars for frontend bundle; remains in U1 backend `.env` only (NFR1.3, C-04) | u3-stats-ui must not call OpenRouter directly. |
| CI credentials (repo/package registry, if any) | Stored in CI secret store with least privilege; not exposed to frontend build output | Use masked secrets; avoid printing env vars. |
| Bundle verification | Deterministic post-build scan gates merges/artifacts | Prevents accidental secret leakage into `dist/`. |

## Rollback Procedures

1. **Identify bad revision**: confirm issue via UI indicators/console diagnostics or integration feedback on LAN deployment.
2. **Revert artifact**: redeploy last known-good `dist/` through U1 static serving (preferred) or revert offending commit and rerun pipeline.
3. **Rebuild & rescan**: if rebuilding, rerun full CI including tests, coverage, and bundle secret scan before serving.
4. **Verify recovery**: reload SPA, confirm `LanRiskBanner`, telemetry connection/reconnect behavior, and absence of console payload leaks/regressions.
5. **Post-rollback**: record defect and corrective change; keep pipeline gates unchanged (coverage/scan not weakenable).

## Assumptions & Open Questions

- Exact CI platform and script names (`scripts/check-dist-secrets.sh`, package manager commands) are finalized at implementation time but must satisfy the behaviors specified above.
- If deployment boundary expands beyond LAN or introduces separate hosting, revisit with ingress/auth, CDN/cache headers, and environment promotion controls.