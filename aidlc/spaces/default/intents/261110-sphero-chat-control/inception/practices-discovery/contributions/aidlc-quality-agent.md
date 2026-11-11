**Collaborator:** aidlc-quality-agent

## Contribution

### Assessment of the lead draft against org.md defaults for mvp scope

The lead draft correctly treats `org.md` as suggested defaults (not established facts) for this greenfield mvp intent, and correctly identifies test-after as the org.md default methodology when no posture has been affirmed, with ordering "implement each applicable testable layer, then write and run that layer's tests." Everything is correctly marked pending interview, and nothing is presented as an established team fact. That is the right stance for greenfield with an empty `team.md`.

Two corrections are needed before the interview:

1. Scope is already known: `aidlc-state.md` records `Scope: mvp`. Under org.md, mvp scope unconditionally adds an **80% line-coverage floor** and **CI execution before merge**. These are additive floors that apply now, not items to defer "once scope is known." The draft should state them as applicable defaults for this intent, subject to interview confirmation.

2. The draft omits the test-pattern layer that a Standard Test Strategy requires: test-pyramid balance (unit > integration > e2e), test independence, per-module coverage of happy path plus at least two error/edge cases (per construction-phase testing standards), and test tooling. For the Python backend this should target pytest + coverage.py; the SPA frontend needs a runner once its stack is chosen.

### Integratable text for team-practices.md — Testing Posture

- **Methodology**: test-after (org.md default for mvp; pending team affirmation)
- **Ordering**: implement each applicable testable layer, then write and run that layer's tests
- **Coverage floor**: 80% line coverage (org.md mvp floor, additive, applies now; may not be weakened to make Build and Test pass)
- **CI execution**: tests run in CI before merge; failure blocks the PR (org.md mvp floor, applies now)
- **Test patterns**: unit > integration > e2e per the test pyramid; tests independent and self-contained; every module covers happy path plus at least two error/edge cases; every defect gets a reproducing test before fix; existing suite must stay green
- **Tooling**: pytest + coverage.py for the Python backend; language-appropriate runner for the SPA frontend once its stack is selected

### For discovered-rules.md

No hard constraints are needed yet — keep Mandated (`ALWAYS`) and Forbidden (`NEVER`) pending the interview. If the team affirms a stricter posture (e.g. TDD or BDD), record it there as an `ALWAYS` rule.

### Gaps to raise at the interview

- Confirm test-after vs TDD/BDD/ATDD as the team's methodology
- Confirm the team accepts the 80% line-coverage floor and CI-before-merge as applicable now (mvp scope)
- Confirm Python backend test tooling (pytest + coverage.py) and frontend test runner once the stack is known
- Confirm who owns CI test execution and coverage enforcement

## Positions

AGREE: test-after as the proposed mvp methodology — matches org.md default when no posture has been affirmed
AGREE: ordering "implement each applicable testable layer, then write and run that layer's tests" — matches org.md and keeps tests layered
AGREE: all practice items marked pending interview — correct for greenfield with no affirmed team practices
AGREE: coverage floors and CI-before-merge are additive scope floors that may not be weakened — matches org.md
OBJECT: coverage floor and CI execution deferred to "once scope is known" — scope is already mvp, so 80% line coverage and CI-before-merge are already applicable defaults, not open interview items
OBJECT: no test patterns specified (pyramid balance, independence, error-case coverage) — leaves Standard Test Strategy volume undefined for Code Generation and CI
OBJECT: no test tooling named — Python backend needs pytest + coverage.py identified now so later stages can target them
OBJECT: no regression policy stated — every defect should produce a reproducing test before fix and the suite must remain green
