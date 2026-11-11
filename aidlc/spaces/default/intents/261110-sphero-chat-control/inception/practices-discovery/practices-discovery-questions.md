# Practices Discovery — Interview Questions

## Sources

- [scope] Workflow-selected scope: `mvp`.
- [org] Suggested defaults from `aidlc/spaces/default/memory/org.md` (greenfield: these are suggestions, not established facts).

## Q1. [Product] Way of Working — How does the team handle branches and merges?

Org.md default: trunk-based development, base `main`, target `main`, squash-merge Bolt branches into `main`.

- A. Trunk-based: one `main` branch, short-lived feature branches squash-merged into `main`
- B. Feature branches with merge commits (not squash)
- C. GitFlow with `develop` and `main` branches
- D. Not yet defined — I'll decide later
- X. Other (please specify)

[Answer]: A. Trunk-based: one `main` branch, short-lived feature branches squash-merged into `main`

## Q2. [Product] Walking Skeleton — Build a thin end-to-end slice first?

A walking skeleton is a minimal version that runs the whole way through, built first to prove the pieces connect before the real features go in.

- A. Yes — build a walking skeleton first (chat → robot → stats end-to-end), then add features
- B. No — skip the skeleton, build features directly
- C. Not yet defined — I'll decide later
- X. Other (please specify)

[Answer]: A. Yes — build a walking skeleton first (chat → robot → stats end-to-end), then add features

## Q3. [Product] Testing Posture — What test methodology does the team use?

Org.md default: test-after (implement first, then write and run tests for each layer). mvp scope adds an 80% line-coverage floor and CI execution before merge.

- A. Test-after — implement first, then write and run tests for each layer
- B. TDD — write tests first, then implement to make them pass
- C. BDD — write scenarios in Given/When/Then, then implement
- D. Custom — a mix of approaches
- X. Other (please specify)

[Answer]: C. BDD — write scenarios in Given/When/Then, then implement

## Q4. [Product] Deployment — How does the team deploy?

Org.md default: deploy on merge to staging; production gates on manual approval (tech lead + product owner).

- A. Deploy on merge to staging; production needs manual approval
- B. Continuous deployment to production on every merge
- C. Manual deployment only, no CI/CD
- D. Not yet defined — I'll decide later
- X. Other (please specify)

[Answer]: B. Continuous deployment to production on every merge

## Q5. [Product] Code Style — How does the team handle formatting and linting?

Org.md default: defer to project-level config (Prettier for JS/TS, Black for Python), linter in CI before merge, failure blocks the PR.

- A. Project-level formatter + linter, CI blocks merge on failure
- B. Team style guide, reviewed manually in PRs
- C. No formal style rules — format however
- D. Not yet defined — I'll decide later
- X. Other (please specify)

[Answer]: A. Project-level formatter + linter, CI blocks merge on failure

## Q6. [Security] Secret Management — How are API keys and secrets handled?

This project uses `.env` for the OpenRouter API key. DevSecOps flag: `.env` must never be committed.

- A. `.env` never committed; secrets from CI/env vars or secrets manager; secret scanning in CI
- B. `.env` committed locally, not shared
- C. Not yet defined — I'll decide later
- X. Other (please specify)

[Answer]: A. `.env` never committed; secrets from CI/env vars or secrets manager; secret scanning in CI
