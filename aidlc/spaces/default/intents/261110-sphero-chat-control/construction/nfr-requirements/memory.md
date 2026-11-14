<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
<!-- example: 2026-05-29T10:14:32Z — chose REST over GraphQL; the consuming team only needs CRUD, revisit if subscriptions land -->
- 2026-11-13T19:35:32Z — [unit u3-stats-ui] Let the unit's refresh and rendering targets carry NFR3.x IDs. Because `produces_kinds` for a `ui` unit ships no reliability or observability file, the reconnect backoff (Q3) and the stale-on-disconnect display (Q4) were recorded as NFR3.4/NFR3.5 under performance rather than invented into files this unit does not produce.
- 2026-11-13T19:35:32Z — [unit u3-stats-ui] Frontend security items inherit NFR1 (LAN-only) as NFR1.2–NFR1.5, continuing after u2's NFR1.1 instead of reusing NFR2 (BLE), since U3 displays the connection status it receives and never touches Bluetooth itself.

## Deviations
<!-- example: 2026-05-29T10:14:32Z — skipped the optional caching layer the stage prose suggested; the dataset is small enough that it adds risk -->

## Tradeoffs
<!-- example: 2026-05-29T10:14:32Z — picked TDD over BDD this run; the team is unit-first and the domain is well-understood -->
- 2026-11-13T19:35:32Z — [unit u3-stats-ui] Tailwind CSS (Q6 option C) chosen over CSS Modules and a component library; it is a Vite build-time dependency only, so no runtime component library is added and native controls keep the NFR5 accessibility bar.
- 2026-11-13T19:35:32Z — [unit u3-stats-ui] Q7 option B's visible event counter and Q5 option A's plain escaped-rendering posture went into tech-stack-decisions.md under client diagnostics, because this unit produces no observability or dedicated security-artifact file beyond security-requirements.md.
- 2026-11-13T19:35:32Z — [unit u3-stats-ui] Kept Q1 option D (no measured latency target) and Q2 option B (render every event) together: the subscription applies every event with no coalescing or throttle, and acceptance is verified behaviourally rather than with a timing assertion.

## Open questions
<!-- example: 2026-05-29T10:14:32Z — confirm the retention window with compliance before the next stage hardens the schema -->
- 2026-11-13T19:35:32Z — [unit u3-stats-ui] Derived NFR IDs are unit-scoped and reuse the same NFRx.y numbers across units (u1 and u2 both define NFR2.1 and NFR4.1). U3 continues NFR1.x/NFR3.x without collision, but a cross-unit ID check at Build and Test would confirm traceability stays unambiguous across the intent.
