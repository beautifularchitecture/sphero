<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-11-20T07:30Z — all four CI Pipeline topic questions were already answered upstream (GitHub Actions from U1 NFR7.2 + the GitHub remote; trunk-based on `main` from practices-discovery Q1; gate set from Q3/Q5 + Build and Test; no artifact repo from the per-unit infrastructure designs and skipped deploy stages), so they were recorded with sources in `ci-pipeline-questions.md` rather than asked again.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-11-20T07:30Z — G6 (lint) is defined in `quality-gates.md` but not wired into `ci.yml`: the repo has no linter dependency/config/script despite team Q5. It is surfaced at the gate rather than faked with a no-op or by weakening another gate.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-11-20T07:30Z — chose one GitHub Actions workflow with two parallel jobs plus an aggregate `ci-ok` required check (fits trunk-based squash-to-`main`) over per-unit workflows; no artifact repository (Q4), so `dist/` is a short-lived workflow artifact.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-11-20T07:30Z — repository owner must enable branch protection requiring `ci-ok`, and must add a repo-level linter/config to activate G6; neither can be set from workflow files.
