<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->
- 2026-11-15T21:51:37Z — loop-back 1: u1 produced no source/tests (pytest exit 4) and u3's hook builds a relative WebSocket URL, so Code Generation reopens for u1-chat-command-core and u3-stats-ui; the gate is not presented on this failed run (see test-results.md `## Loop-Back Log`).
- 2026-11-15T21:51:37Z — added `@vitest/coverage-v8@1.6.0` as a devDependency so the U3 80% floor could be measured (90.58%) instead of left unverified; ran `python3` in place of the recorded `python` because no `python` alias exists on this host.

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
