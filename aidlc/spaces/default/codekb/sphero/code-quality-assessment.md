# Code Quality Assessment — sphero

## Test Coverage and Methodology

- **Structure**: BDD Given/When/Then scenarios in all three suites (Python test names `test_given_..._when_..._then_...`; Vitest `it('Given ... When ... Then ...')`). Offline doubles (fake sockets, scripted model clients, fake BLE clients, `MockWebSocket`) keep suites self-contained — no key, network or robot required.
- **Floors**: 80% line coverage enforced by CI for U1 (`tests/`), U2 (`u2_telemetry/`) and the SPA (Vitest v8 thresholds). `pyproject.toml:24` also sets `fail_under = 80` with branch coverage. CI blocks merge on failure.
- **Key suites**: U1 walking-skeleton integration (`tests/integration/test_walking_skeleton.py`) exercises chat → agent → BLE write → ack and error/stop paths; U2 service integration (`u2_telemetry/tests/test_service.py`) exercises normalize → publish, lenient placeholders and error/status callbacks; U3 integration (`frontend/src/integration-websocket-to-ui.test.tsx`) exercises telemetry frame → rendered fields, reconnect and malformed-frame handling.
- **Verification commands recorded in-repo**: README says `pytest` plus a planned coverage command; CI uses two unit-scoped commands (`python -m pytest tests/ ... --cov-fail-under=80`, `python -m pytest u2_telemetry/ ... --cov-fail-under=80`). The bare `pytest` conflicts with `testpaths = ["u2_telemetry/tests"]`.

## Linting, Typechecking, CI/CD

- **Frontend**: `npm run typecheck` (`tsc --noEmit`) gates CI; no ESLint config or lint step. One `eslint-disable-next-line react-hooks/exhaustive-deps` in `useRobotStateConnection.ts:263` with no linter to consume it.
- **Backend**: no Black/Ruff/mypy config or CI step; `.github/copilot-instructions.md` names them as intended checks only.
- **CI**: `.github/workflows/ci.yml` runs on push/PR to `main` with concurrency cancellation; frontend job includes a bundle secret scan for OpenRouter key patterns; backend job installs `requirements.txt` and runs both pytest suites; `ci-ok` aggregates. Continuous deployment is not configured in-repo.
- **Secret hygiene**: `.gitignore` excludes `.env` / `.env.*`; U1 settings redact the key from logs and `repr` (`backend/app/config.py:67-78`); no hardcoded credentials found.

## Documentation Quality

README documents hardware prerequisites, Bluetooth setup, BLE discovery, LED/drive smoke checks and verification, but is stale about the application itself (see below). `DEPLOYMENT-u2-telemetry.md` covers U2 installation, systemd service, configuration, contracts and observability. `.github/copilot-instructions.md` records architecture and conventions with an explicit "verify what is implemented" caveat. Production modules carry substantial docstrings.

## Technical Debt and Risks

- **Stale README status**: `README.md:8-14` claims the app is still being designed and that the checks do not test the web app/WebSocket/agent/UI, while all three units are implemented with run scripts and CI. No "how to run the app" section exists — the direct target of the current intent.
- **Undeclared runtime dependency**: `uvicorn` is used by both backends but absent from `requirements.txt` / `pyproject.toml`.
- **BLE identity mismatch**: U1 control UUIDs (`6e400001-…` / `6e400002-…`, `config.py:25-26`) differ from the Sphero vendor service in the README and U2's telemetry characteristic (`ble_listener.py:18`).
- **Broad exception suppression**: 9 `# noqa: BLE001` / `type: ignore` sites at BLE/publish boundaries, each with a rationale; no TODO/FIXME/HACK markers found. One intentional `eslint-disable` note.
- **Security posture**: no authentication or rate limiting on `/ws/chat` or `/ws/robot-state`; accepted LAN-only risk is surfaced by an always-visible banner (`LanRiskBanner`).
- **Stale review note**: `RESPONSE.md` records a NOT-READY advisory review from an earlier design iteration with unresolved contract-direction and normalization contradictions; verify against current code before treating it as current.
