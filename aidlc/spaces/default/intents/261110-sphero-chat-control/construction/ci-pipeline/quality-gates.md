# Quality Gates — sphero-chat-control

## Sources

- [practices] `aidlc/spaces/default/memory/team.md` — BDD, 80% line floor, tests in CI before merge, failure blocks merge (Q3); project formatter/linter blocks merge on failure (Q5).
- [build] `construction/build-and-test/build-and-test-summary.md` §3 and §4 — coverage floors of 91.26% (U1), 94.42% (U2) and 94.02% (U3), all above 80%.
- [build] `construction/build-and-test/test-results.md` §1 — the exact commands and outcomes on the passing replay.
- [design] `construction/u3-stats-ui/infrastructure-design/cicd-pipeline.md` — bundle secret scan gate (NFR1.3).
- [config] `ci-config.md` — the `frontend` and `backend` jobs that enforce these gates.

## Gate definitions

| ID | Gate | Pass criterion (not weakenable to make a step pass) | Enforced by | Source |
|---|---|---|---|---|
| G1 | Type check | `npm run typecheck` (`tsc --noEmit`) exits 0 with no diagnostics | `frontend` job | Build and Test command 2 |
| G2 | Frontend unit/component tests | `npx vitest run` — all 11 files / 65 tests pass, 0 failures | `frontend` job | Build and Test command 5 |
| G3 | Frontend coverage floor | Whole `frontend/src` ≥ 80% line coverage (measured 94.02%); `--coverage.thresholds.lines=80` | `frontend` job | team Q3 floor; Build and Test §3 |
| G4 | Production build | `npm run build` exits 0 and emits `dist/` | `frontend` job | Build and Test command 1 |
| G5 | Bundle secret scan | No `OPENROUTER_API_KEY`, `VITE_OPENROUTER_API_KEY` or `sk-or-` match in `dist/` or `frontend/src/` | `frontend` job | U3 design NFR1.3 |
| G6 | Lint / format check | Zero lint errors; failure blocks merge | **Not wired — see Open items** | team Q5 |
| G7 | U1 backend tests | `python -m pytest tests/ --cov=backend/app` — all 100 tests pass | `backend` job | Build and Test command 3 |
| G8 | U1 coverage floor | ≥ 80% line/branch coverage (measured 91.26%); `--cov-fail-under=80` | `backend` job | team Q3 floor |
| G9 | U2 telemetry tests | `python -m pytest u2_telemetry/ --cov=u2_telemetry` — all 53 tests pass | `backend` job | Build and Test command 4 |
| G10 | U2 coverage floor | ≥ 80% line coverage (measured 94.42%); `--cov-fail-under=80` | `backend` job | team Q3 floor |
| G11 | Aggregate merge check | `ci-ok` succeeds only when both `frontend` and `backend` pass; configured as the required branch-protection check on `main` | `ci-ok` job | team Q1 trunk-based strategy |

## Gate behaviour

- Every gate is pass/fail: a failure blocks promotion of that job and, through `ci-ok`, blocks merge. No gate uses `continue-on-error` or a lowered threshold.
- Coverage floors are additive and not weakenable to make Build and Test pass (org.md testing posture; team Q3).
- Frontend and backend jobs run in parallel; `ci-ok` is the single required status check, so a squash merge to `main` (team Q1) cannot land with a red job.
- G1–G5 and G7–G10 are enforced by concrete commands that passed on the fresh Build and Test replay.

## Deferred gates (not enforced in this MVP workflow)

The Standard test strategy and this plan do not schedule the following; they are recorded so no gate is silently presumed green:

| Concern | Status | Owner / reason |
|---|---|---|
| Real-browser UI verification (NFR3.2–NFR3.5 u3) | `Unverified` | No browser engine ran the jsdom checks; no performance/e2e stage scheduled |
| BLE-hardware timing (NFR4.1–NFR4.4 u1, NFR4.1–NFR4.3 u2, NFR2.1 u2) | `Unverified` | No Sphero Mini / BLE adapter; `performance-validation` is `[S]` |
| SAST / DAST security scans | Not configured | Standard strategy; no security stage in this plan |
| Continuous deployment to the LAN host | Team practice, not automated here | `deployment-pipeline` / `environment-provisioning` are `[S]` |

## Assumptions & Open Questions

- **G6 (lint) is defined but not enforced.** Team Q5 requires a project-level formatter/linter with CI blocking on failure, but the repository has no linter dependency, config or `lint` script (no ESLint/Prettier/Ruff/Black present). Wiring it is a follow-up: add the tool and repo-root config, fix any findings, then add the step to the `frontend` and `backend` jobs. It is deliberately not faked with a no-op step, and no other gate is weakened to compensate. Surfaced at the CI Pipeline completion gate.
- Branch protection (requiring `ci-ok`) is a repository setting and cannot be set from workflow files; it must be enabled by the repository owner.
- None of the coverage figures here were re-measured in CI — they are the passing local Build and Test values; CI re-runs the same commands and enforces the floors on each push/PR.
