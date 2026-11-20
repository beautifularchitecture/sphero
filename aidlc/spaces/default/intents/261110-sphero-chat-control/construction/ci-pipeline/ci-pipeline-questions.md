# CI Pipeline — Clarifying Questions

## Sources

- [scope] Workflow-selected scope: `mvp`.
- [practices] Team practices affirmed at practices-discovery Q1 (trunk-based on `main`, short-lived branches squash-merged), Q3 (BDD, 80% line floor, CI before merge), Q4 (continuous deployment on every merge), Q5 (project-level formatter/linter, CI blocks merge on lint failure).
- [repo] Git remote `origin` → `https://github.com/beautifularchitecture/sphero.git`; current branch `main`; no CI workflow present under `.github/workflows/`.
- [design] `construction/u1-chat-command-core/nfr-design/reliability-design.md` NFR7.2 — GitHub Actions workflow on push/PR, block merge on failure.
- [design] Per-unit `construction/<unit>/infrastructure-design/cicd-pipeline.md` for u1, u2 and u3.
- [build] `construction/build-and-test/build-and-test-summary.md` and `test-results.md` — the exact commands, coverage floors and fresh evidence.

All four topic questions are already answered by prior stages or by the repository itself. They are recorded here with their source rather than asked again (Construction-stage questions are exceptional, and an answered question is never re-asked).

## Q1. [Pipeline & Deploy] Which CI tool runs the merge gates?

The repository is hosted on GitHub and U1's reliability design already specifies a GitHub Actions workflow on push/PR. Which runner executes the gates?

- A. GitHub Actions on push and pull requests (carried forward from U1 NFR7.2)
- B. AWS CodePipeline / CodeBuild
- C. Jenkins or GitLab CI
- D. Other (please specify)

[Answer]: A. GitHub Actions on push and pull requests — grounded in the GitHub `origin` remote and `u1-chat-command-core/nfr-design/reliability-design.md` NFR7.2.

## Q2. [Pipeline & Deploy] What branch strategy does the pipeline protect?

Merges to `main` are the release trigger; the pipeline's branch protection must match the affirmed strategy.

- A. Trunk-based on `main`; short-lived branches squash-merged (affirmed at practices-discovery Q1)
- B. Feature branches with merge commits
- C. GitFlow with `main` and `develop`
- D. Other (please specify)

[Answer]: A. Trunk-based on `main`; short-lived branches squash-merged — affirmed at practices-discovery Q1 and recorded in `team.md > Way of Working`.

## Q3. [Pipeline & Deploy] Which quality gates must pass before merge?

Build and Test fixed the exact commands and the 80% line-coverage floor; team practices require lint and tests in CI before merge.

- A. Type-check, unit + integration tests, 80% line floor, production build and bundle secret scan; any failure blocks merge (affirmed Q3/Q5 plus Build and Test)
- B. Tests only
- C. Manual code review only
- D. Other (please specify)

[Answer]: A. Type-check, unit + integration tests, 80% line floor, production build and bundle secret scan; any failure blocks merge — affirmed at practices-discovery Q3 and Q5; commands fixed by `build-and-test/build-and-test-summary.md`.

## Q4. [Pipeline & Deploy] Which artifact repositories are used?

The MVP is a LAN-only app: U3 produces a static `dist/` bundle served by U1, and U2/U1 deploy Python source to a local Linux host. No container or cloud deployment stage is in this plan.

- A. None — static `dist/` bundle and Python source, deployed to the LAN host; no container/cloud registry in this MVP
- B. Amazon ECR / CodeArtifact / S3
- C. GitHub Packages
- D. Other (please specify)

[Answer]: A. None — static `dist/` bundle and Python source, deployed to the LAN host — grounded in the per-unit infrastructure designs; `deployment-pipeline` and `environment-provisioning` are `[S]` (skipped) in this plan.

## Assumptions & Open Questions

- **Lint tooling gap:** Q5 affirms a project-level formatter/linter with CI blocking on failure, but no linter is configured in the repository — there is no ESLint/Prettier/Ruff/Black dependency or config, and no `lint` script. The workflow enforces every gate with a concrete passing command except lint; see `quality-gates.md` G6 and the completion gate.
- **Deployment scope:** Continuous deployment to the LAN host remains the team's affirmed practice, but concrete deploy automation is owned by the skipped `deployment-pipeline` stage. This stage delivers CI gates only.
- **Evidence gaps carried from Build and Test:** real-browser U3 behaviour and BLE-hardware timing remain `Unverified`; CI enforces the automated gates only and does not fabricate browser or robot evidence.
