# CI Configuration — sphero-chat-control

## Sources

- [questions] `ci-pipeline-questions.md` — Q1 GitHub Actions, Q2 trunk-based on `main`, Q3 gate set, Q4 no artifact repository.
- [practices] `aidlc/spaces/default/memory/team.md` — trunk-based on `main` (Q1), BDD + 80% line floor + CI before merge (Q3), continuous deployment on every merge (Q4), project formatter/linter blocks merge (Q5).
- [build] `construction/build-and-test/build-and-test-summary.md` and `test-results.md` — the exact, freshly-passing commands and coverage floors.
- [design] `construction/u3-stats-ui/infrastructure-design/cicd-pipeline.md` — checkout/install, lint, type-check, tests, coverage, build, bundle secret scan, handoff.
- [design] `construction/u1-chat-command-core/infrastructure-design/cicd-pipeline.md`, `construction/u2-telemetry/infrastructure-design/cicd-pipeline.md` — backend build/test/deploy stages.
- [repo] GitHub remote `origin`; branch `main`; no workflow present under `.github/workflows/` before this stage.

## Pipeline overview

A single GitHub Actions workflow, `.github/workflows/ci.yml`, runs on every push to `main` and on every pull request into `main`. Two parallel jobs — `frontend` (U3) and `backend` (U1 + U2) — enforce the Build and Test commands and coverage floors. A final `ci-ok` job aggregates both and is the single required status check for branch protection, matching the trunk-based, squash-to-`main` strategy.

Per Q4 there is no artifact repository: the `frontend` job uploads `dist/` as a short-lived workflow artifact for the U1 static-serving handoff, and the backend jobs operate on Python source. Continuous deployment to the LAN host is the team's affirmed practice but is owned by the skipped `deployment-pipeline` stage; this stage delivers CI gates only.

## Workflow configuration

The concrete file is `.github/workflows/ci.yml` at the repository root. Its content:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  frontend:
    name: Frontend — typecheck, test, coverage, build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm
      - name: Install dependencies
        run: npm ci
      - name: Type check
        run: npm run typecheck
      - name: Unit and component tests with 80% line floor
        run: >-
          npx vitest run --coverage --coverage.provider=v8
          --coverage.include='frontend/src/**/*.{ts,tsx}'
          --coverage.exclude='frontend/src/**/*.test.{ts,tsx}'
          --coverage.exclude='frontend/src/test-utils/**'
          --coverage.exclude='frontend/src/test-setup.ts'
          --coverage.reporter=text --coverage.thresholds.lines=80
      - name: Production build
        run: npm run build
      - name: Bundle secret scan
        run: |
          if grep -RInE 'OPENROUTER_API_KEY|VITE_OPENROUTER_API_KEY|sk-or-' dist frontend/src; then
            echo "Potential secret detected in frontend source or bundle"
            exit 1
          fi
      - name: Upload SPA bundle
        uses: actions/upload-artifact@v4
        with:
          name: spa-dist
          path: dist/
          retention-days: 14

  backend:
    name: Backend — U1 and U2 tests with coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14'
          cache: pip
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements.txt
      - name: U1 backend tests (80% floor)
        run: python -m pytest tests/ --cov=backend/app --cov-report=term-missing --cov-fail-under=80
      - name: U2 telemetry tests (80% floor)
        run: python -m pytest u2_telemetry/ --cov=u2_telemetry --cov-report=term-missing --cov-fail-under=80

  ci-ok:
    name: CI passed
    runs-on: ubuntu-latest
    needs: [frontend, backend]
    steps:
      - run: echo "All CI gates passed"
```

## Job details

| Job | Steps | Locally verified command evidence |
|---|---|---|
| `frontend` | `npm ci`, `npm run typecheck`, Vitest + v8 coverage (`thresholds.lines=80`), `npm run build`, bundle secret scan, upload `dist/` | Build and Test: typecheck clean; 65 tests / 11 files pass; 94.02% lines; build 41 modules; no secret match |
| `backend` | pip install, U1 `pytest tests/ --cov=backend/app`, U2 `pytest u2_telemetry/ --cov=u2_telemetry` | Build and Test: 100 passed / 91.26%; 53 passed / 94.42%; both `--cov-fail-under=80` satisfied |
| `ci-ok` | aggregates `frontend` + `backend`; the required branch-protection check | — |

Command notes:

- `npm ci` uses the committed `package-lock.json`, so installs are reproducible. The local host has no `python` shim (`/usr/bin/python3` only); CI uses `python` from `actions/setup-python`, which is correct on the runner.
- `--coverage.thresholds.lines=80` is a global floor, not a per-file one; `src/main.tsx` (entrypoint, 0%) does not fail it, matching the whole-module 80% floor agreed in Build and Test.
- `pyproject.toml` already sets `[tool.coverage.report] fail_under = 80` and `branch = true`; `--cov-fail-under=80` restates the U1 floor at the command level.

## Artifacts and promotion

- `spa-dist` — the U3 `dist/` static bundle, retained 14 days, traceable to the commit SHA via the workflow run. Consumed by U1 static serving; no container registry (Q4).
- No staging/production artifact promotion in this workflow — owned by the skipped deployment stages.

## Secrets

- `OPENROUTER_API_KEY` stays in the backend `.env` on the LAN host and is never injected into the frontend build (NFR1.3). The bundle secret scan fails the `frontend` job on any key/token reference.
- No CI secrets are required for these gates. The project rule "NEVER commit `.env` or `.env.*`" remains in force.

## Assumptions & Open Questions

- Lint is defined as a required gate (team Q5) but is **not wired** here: no linter dependency, config or script exists in the repo. Adding it must not weaken the other gates; see `quality-gates.md` G6.
- `actions/*` major versions and `node-version: '20'` / `python-version: '3.14'` follow the current toolchain; Python 3.14 satisfies `requires-python = ">=3.14"`.
- Branch protection must be configured in the GitHub repository to require the `ci-ok` check before merge; this file defines the check but cannot set repository settings.
