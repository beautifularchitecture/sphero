# Team Practices — Affirmed (Practices Discovery)

Affirmed team practice established at the practices-discovery interview. These
are established team facts, matching the five practice sections of
`aidlc/spaces/default/memory/team.md`. No draft markers remain.

## Way of Working

Trunk-based development on `main`: one `main` branch, short-lived feature
branches squash-merged into `main` as one commit named by the Bolt slug, with
the Bolt's own commits left on the source branch until the worktree is
discarded. One trunk gates releases with tags or environment-specific
deployment configs rather than long-lived release branches.

Affirmed at interview Q1: trunk-based development on `main`, squash-merged
feature branches.

## Walking Skeleton

On — build the walking skeleton first: a thin end-to-end slice (chat → robot →
stats) that proves the pieces connect before the real features go in. Features
are added on top of the verified skeleton.

Affirmed at interview Q2: walking skeleton on (build skeleton first, then add
features).

## Testing Posture

- **Methodology**: bdd
- **Methodology evidence**: BDD — write scenarios in Given/When/Then, then
  implement to make them pass (interview Q3 answer). org.md requires the
  testing methodology to be affirmed at practices-discovery and recorded under
  `## Testing Posture` with explicit `Methodology` and `Ordering` fields.
- **Ordering**: Write scenarios in Given/When/Then first, then implement, then
  run tests.
- **Coverage floor**: 80% line coverage (mvp scope floor per org.md; additive,
  applies now for this intent; may not be weakened to make Build and Test
  pass).
- **CI execution**: tests run in CI before merge; failure blocks merge.
- **Test patterns**: unit > integration > e2e per the test pyramid; tests
  independent and self-contained; every module covers the happy path plus at
  least two error/edge cases.
- **Tooling**: pytest + coverage.py for the Python backend; language-appropriate
  runner for the SPA frontend once its stack is selected.

Affirmed at interview Q3: BDD methodology with scenarios-first ordering.

## Deployment

Continuous deployment to production on every merge. Every commit that passes the
quality gates auto-deploys to production; this is a team decision, not a
framework default.

Affirmed at interview Q4: continuous deployment to production on every merge.

## Code Style

Project-level formatter and linter configured in repo root; linter runs in CI
before merge; failure blocks merge on lint failure. Language-idiomatic naming
(camelCase for JS/TS, snake_case for Python, etc.). No project-wide rename
rules unless the team affirms one.

Affirmed at interview Q5: project-level formatter + linter, CI blocks merge on
failure.
