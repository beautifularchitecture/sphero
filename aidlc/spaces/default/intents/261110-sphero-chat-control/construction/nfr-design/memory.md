<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
2026-11-12T04:58:00Z — NFR Design for u2-telemetry: async publish (Q2=A) keeps BLE reception non-blocking at NFR4.2's 10 events/sec; correlation IDs (Q4=A) make fire-and-forget events traceable without per-event logging.

## Deviations
<!-- none -->

## Tradeoffs
2026-11-12T04:58:00Z — no circuit breaker (Q1=A) and single logical RobotTelemetry component (Q5=A): simplicity over extensibility for the single-robot MVP, matching NFR2.3's retry-with-backoff exactly.

## Open questions
<!-- none -->
