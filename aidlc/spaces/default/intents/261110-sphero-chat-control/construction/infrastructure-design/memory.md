<!-- INVARIANT: examples are single-line HTML comments so a fresh template parses to total=0 (MEMORY_EMPTY). Do NOT un-comment or split across lines. t100 guards this. -->
> This file is kept up to date automatically while the stage runs. Add observations at the review step, not by editing here directly.

## Interpretations
2026-11-12T05:10:00Z — Infrastructure Design for u2-telemetry: single Linux host with BLE radio running Python/bleak/FastAPI as a systemd service; no containers/CDK needed for the single-robot MVP since BLE requires direct hardware access.

## Deviations
<!-- none -->

## Tradeoffs
2026-11-12T05:10:00Z — rolling deployment instead of blue-green/canary (single host, double cost unjustified); no persistent data store (telemetry is fire-and-forget per Contract 2); U2 has no secrets (NFR2.2), all secret management lives in U1.

## Open questions
<!-- none -->
