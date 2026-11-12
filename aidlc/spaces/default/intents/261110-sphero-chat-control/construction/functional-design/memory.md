<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
2026-11-12T06:05:00Z — Functional Design for u3-stats-ui: UI unit (StatsDisplay SPA) subscribing to U2's RobotStateChanged events via WebSocket per Contract 2; rendering robot state, connection status, and error messages per US1.4/US1.5.

## Deviations
<!-- none -->

## Tradeoffs
2026-11-12T06:05:00Z — split component architecture (StatsPanel + RobotStateDisplay + ConnectionStatus + SpeedColorSelector + ErrorMessage) instead of single component, per Q1=B; WebSocket subscription instead of polling, per Q2=A; speed/color buttons send chat commands through existing path, per Q4=A.

## Open questions
<!-- none -->
