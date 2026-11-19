# Cross-Unit Traceability — sphero-chat-control

Stage: `build-and-test` (3.6) · Source: `aidlc engine sensor-traceability --stage build-and-test`
Run: 2026-11-15 (UTC)

## Verdict

**FAIL** — `pass: false`. 21 requirement/acceptance IDs are uncovered; the
coverage rows that do exist are concentrated in U2 and U3, while U1 contributes
no implementation or tests.

## Sensor output summary

| Metric | Value |
|---|---|
| `pass` | `false` |
| Uncovered IDs | 21 |
| Covered IDs | 10 (`FR3`, `FR4`, `NFR1`, `AC1.4.1`, `AC1.4.2`, `AC1.5.1`–`AC1.5.4`) |
| Units represented in coverage | `u2-telemetry`, `u3-stats-ui` (no `u1-chat-command-core` implementation) |

## Per-ID coverage

| ID | Covered | Built in / blocking reason | Owning stage / Unit | Verdict |
|---|---|---|---|---|
| FR1.1 | No | AC1.1.1–AC1.1.5 all `not_built`; no U1 source | code-generation / u1-chat-command-core | **Uncovered** |
| FR1.2 | No | AC1.2.1–AC1.2.3 all `not_built` | code-generation / u1 | **Uncovered** |
| FR2 | No | AC1.3.1–AC1.3.3 all `not_built` | code-generation / u1 | **Uncovered** |
| FR3 | Yes | `ErrorDisplay.tsx` (AC1.5.1–AC1.5.4) | u3-stats-ui | Covered |
| FR4 | Yes | `ErrorDisplay.tsx` (AC1.5.1–AC1.5.4) | u3-stats-ui | Covered |
| NFR1 | Yes | `u3: NFR1.2–NFR1.5` | u3-stats-ui | Covered |
| NFR2 | No | `u1: NFR2.1, NFR2.2` not built; U2 rows OK | code-generation / u1 | **Uncovered** |
| NFR3 | No | `u1: NFR3.1–NFR3.6` not built; U3 rows OK | code-generation / u1 | **Uncovered** |
| NFR4 | No | `u1: NFR4.1–NFR4.5` not built; U2/U3 rows OK | code-generation / u1 | **Uncovered** |
| NFR5 | No | no coverage row in any unit (accessibility posture) | u3-stats-ui (no mapping) | **Uncovered** |
| NFR6 | No | no coverage row (test tooling; proven by green runs, not traced) | build-and-test / all units (no mapping) | **Uncovered** |
| NFR7 | No | only `u1: NFR7.1–NFR7.3` rows, all not built; U2/U3 floors met but untraced | build-and-test, ci-pipeline / u1 (no mapping) | **Uncovered** |
| NFR8 | No | only `u1: NFR8.1`, not built; U2/U3 BDD untraced | all units (no mapping) | **Uncovered** |
| AC1.1.1 | No | chat input validation not implemented | code-generation / u1 | **Uncovered** |
| AC1.1.2 | No | agent translation not implemented | code-generation / u1 | **Uncovered** |
| AC1.1.3 | No | robot command not implemented | code-generation / u1 | **Uncovered** |
| AC1.1.4 | No | chat UI not implemented | code-generation / u1 | **Uncovered** |
| AC1.1.5 | No | error path not implemented | code-generation / u1 | **Uncovered** |
| AC1.2.1 | No | speed command path not implemented | code-generation / u1 | **Uncovered** |
| AC1.2.2 | No | speed validation not implemented | code-generation / u1 | **Uncovered** |
| AC1.2.3 | No | speed feedback not implemented | code-generation / u1 | **Uncovered** |
| AC1.3.1 | No | color command path not implemented | code-generation / u1 | **Uncovered** |
| AC1.3.2 | No | color validation not implemented | code-generation / u1 | **Uncovered** |
| AC1.3.3 | No | color feedback not implemented | code-generation / u1 | **Uncovered** |
| AC1.4.1 | Yes | `u2_telemetry/ble_listener.py`, `u3: useRobotStateConnection.ts` | u2 + u3 | Covered (U3 browser path defective — see NFR3.1) |
| AC1.4.2 | Yes | `u2_telemetry/service.py`, `u3: LanRiskBanner.tsx` | u2 + u3 | Covered |
| AC1.5.1 | Yes | `u3: ErrorDisplay.tsx` | u3-stats-ui | Covered |
| AC1.5.2 | Yes | `u3: ErrorDisplay.tsx` | u3-stats-ui | Covered |
| AC1.5.3 | Yes | `u3: ErrorDisplay.tsx` | u3-stats-ui | Covered |
| AC1.5.4 | Yes | `u3: ErrorDisplay.tsx` | u3-stats-ui | Covered |

## Sensor blocking reasons (verbatim)

The sensor reports U1 traceability targets as missing because those rows carry
bare filenames that resolve relative to
`construction/u1-chat-command-core/code-generation/` instead of
`construction/u1-chat-command-core/nfr-design/`:

```
u1-chat-command-core: NFR2.1, NFR2.2: target file does not exist: security-design.md
u1-chat-command-core: NFR3.1–NFR3.6: target file does not exist: observability-design.md
u1-chat-command-core: NFR4.1–NFR4.5: target file does not exist: performance-design.md
u1-chat-command-core: NFR7.1–NFR7.3, NFR8.1: target file does not exist: reliability-design.md
```

The design files themselves do exist under `u1-chat-command-core/nfr-design/`;
the traceability rows are mis-pathed. Even with the paths corrected the rows
would still be unsupported, because they claim design-document coverage while no
implementation or test file exists for U1.

## Findings to surface

1. **U1 is entirely untraced in code.** FR1.1, FR1.2, FR2 and all nine
   acceptance criteria AC1.1.x–AC1.3.x have no implementation.
2. **Cross-cutting NFRs are not mapped anywhere.** NFR5 (accessibility),
   NFR6 (test tooling), NFR7 (coverage floor/CI) and NFR8 (BDD) have no
   traceability rows in U2 or U3, so the sensor cannot see the work that does
   satisfy them. This is an artefact gap for the loop-back replay.
3. **U1 traceability target paths are wrong** (bare filenames, wrong directory).
4. **U3's covered rows overstate readiness.** `AC1.4.1` is marked built in
   `useRobotStateConnection.ts`, but the hook's relative WebSocket URL prevents a
   real connection (see `test-results.md` F2).

## Repair scope for loop-back 1

- Regenerate U1 implementation + tests, then re-map FR1.1, FR1.2, FR2 and
  AC1.1.1–AC1.3.3 to real files.
- Correct U1 NFR targets to `../nfr-design/<file>` and keep them only when the
  implementation exists.
- Add NFR5–NFR8 coverage rows in the owning units (or a documented `N/A` with a
  reason) so the final gate can pass.
