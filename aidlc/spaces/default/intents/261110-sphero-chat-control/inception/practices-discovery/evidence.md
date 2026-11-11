# Evidence — Practices Discovery

## Inspected (this turn)

- `aidlc/spaces/default/memory/org.md` — all five sections read as suggested
  defaults for this greenfield intent: Way of Working, Walking Skeleton, Testing
  Posture, Deployment, Code Style.
- `aidlc/spaces/default/memory/team.md` — all five practice sections empty
  (placeholders only); nothing affirmed by the team yet.
- `aidlc/spaces/default/memory/project.md` — all sections empty (placeholders
  only); no project specialisation recorded yet.
- `aidlc/spaces/default/intents/261110-sphero-chat-control/inception/practices-discovery/memory.md`
  — stage observation diary (empty template, no prior entries).
- `aidlc engine now` — timestamp `2026-11-11T00:49:17Z`.
- `git rev-parse HEAD` — commit `8a68b4f3074e5554d16da3ec735fbbce25408b1b`.

## Support agent contributions (assessed as evidence)

### aidlc-quality-agent

**File:** `contributions/aidlc-quality-agent.md`

Assessment:
- Confirmed the lead draft correctly treats `org.md` as suggested defaults (not
  established facts) for this greenfield mvp intent, and correctly identifies
  test-after as the org.md default methodology when no posture has been
  affirmed, with ordering "implement each applicable testable layer, then write
  and run that layer's tests."
- Correction 1: scope is already known (`aidlc-state.md` records `Scope: mvp`).
  Under org.md, mvp scope unconditionally adds an 80% line-coverage floor and
  CI execution before merge. These are additive floors that apply now, not items
  to defer "once scope is known."
- Correction 2: the draft omits the test-pattern layer that a Standard Test
  Strategy requires: test-pyramid balance (unit > integration > e2e), test
  independence, per-module coverage of happy path plus at least two error/edge
  cases (per construction-phase testing standards), and test tooling. For the
  Python backend this should target pytest + coverage.py; the SPA frontend needs
  a runner once its stack is chosen.
- Positions: AGREE test-after as the proposed mvp methodology; AGREE ordering;
  AGREE all practice items marked pending interview; AGREE coverage floors and
  CI-before-merge are additive and may not be weakened; OBJECT coverage floor
  and CI execution deferred to "once scope is known"; OBJECT no test patterns
  specified; OBJECT no test tooling named; OBJECT no regression policy stated.

### aidlc-developer-agent

**File:** `contributions/aidlc-developer-agent.md`

Assessment:
- Code Style: defer formatter/linter to project-level config with CI blocking
  merge on lint failure. Add type-safety rules (no implicit any/untyped
  parameters, explicit return types on public functions, const by default),
  docstrings/JSDoc on public APIs and exported types, import ordering and quote
  style per formatter config, max line length 100.
- Naming Conventions: camelCase (JS/TS)/snake_case (Python) for variables and
  functions; PascalCase for classes/types/interfaces/components;
  SCREAMING_SNAKE_CASE for constants and enum members; kebab-case (JS/TS)/
  snake_case (Python) files; one module per file; no project-wide rename rules
  unless affirmed.
- Layer Boundaries: four layers (API/presentation, service/application, domain,
  data access/infrastructure); dependencies flow inward only; each layer owns
  its own DTOs/models mapped at boundaries.
- Error Handling: fail fast/fail loud; validate inputs at system boundaries;
  distinguish recoverable vs fatal errors; standardize error types per layer;
  no exceptions across service-layer boundaries without a declared contract;
  prefer Result<T, E>.
- File Organization: feature/domain directories, colocated tests, barrel files
  only for public surface, separate source from config/scripts.
- Positions: AGREE trunk-based development, test-after methodology, deploy on
  merge to staging with manual production approval, defer formatter/linter to
  project config; OBJECT no layer-boundary convention, no error-handling
  convention, no file-organization convention, incomplete naming conventions.

### aidlc-devsecops-agent

**File:** `contributions/aidlc-devsecops-agent.md`

Assessment:
- Secret management: `.env` must never be committed to version control — add
  `.env` and `.env.*` to `.gitignore`, serve secrets from CI-protected
  environment variables or a secrets manager, run secret detection
  (gitleaks/trufflehog) as pre-commit check and CI scan, rotate and purge any
  key already committed.
- Dependency scanning: integrate vulnerability scanning into CI (npm audit/
  Snyk/equivalent) so new and transitive vulnerabilities fail the build above an
  agreed severity threshold; scan on every PR and on a recurring schedule.
- SAST/DAST: add SAST to CI as a blocking security gate; schedule DAST against
  deployed staging endpoints before production promotion; security findings must
  block merge at agreed severity.
- Lint/format: extend the linter with security rules (ESLint security plugin,
  Ruff bandit for Python, or equivalent) so insecure patterns are caught at
  lint time.
- Supply-chain controls: pin direct dependencies in a committed lockfile; vet
  third-party packages before adoption; generate an SBOM for each release
  artifact; verify artifact integrity/signature.
- Positions: AGREE deploy on merge to staging with manual production approval;
  AGREE linter in CI blocking merge; AGREE trunk-based development; OBJECT code
  style omits SAST/dependency scanning/secret detection; OBJECT no rule that
  `.env` must never be committed; OBJECT no supply-chain controls stated.

## Inferred

- Project type: greenfield (no existing code, no reverse-engineering
  artifacts), so `org.md` sections are suggested defaults, not established facts.
- No conversation-language signal found yet in `project.md` or the initial
  description; language resolution will follow the delegated brief's
  `Conversation language:` line first.
- Nothing had been affirmed for this team before the interview: no branching
  strategy, skeleton setting, testing methodology, coverage floor, deployment
  targets, promotion gates, approval owners, or code-style tooling.
- Support agents agreed on trunk-based development, test-after methodology, and
  deploy-on-merge-to-staging with manual production approval prior to the
  interview; the interview superseded the org defaults where the team chose
  otherwise (BDD over test-after; walking skeleton on; continuous deployment to
  production over manual approval).

## Interview Decisions (evidence)

All six interview questions were answered at the practices-discovery interview
and are recorded here as established team facts:

- Q1 Way of Working: trunk-based development on `main`; short-lived feature
  branches squash-merged into `main`.
- Q2 Walking Skeleton: on — build the walking skeleton first (chat → robot →
  stats end-to-end), then add features.
- Q3 Testing Methodology: BDD — write scenarios in Given/When/Then, then
  implement.
- Q4 Deployment: continuous deployment to production on every merge.
- Q5 Code Style: project-level formatter + linter; CI blocks merge on failure.
- Q6 Secret Management: `.env` never committed; secrets from CI/env vars or
  secrets manager; secret scanning in CI.
