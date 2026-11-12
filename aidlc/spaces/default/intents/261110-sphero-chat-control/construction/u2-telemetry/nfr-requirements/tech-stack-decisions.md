# Tech Stack Decisions — u2-telemetry

Grounded in functional-spec [functional-spec], rules [rules], requirements [requirements], contract-summary [contract-summary], and nfr-requirements questions [nfr-requirements-questions].

## Technology Selections

| Layer | Technology | Version | Rationale | Source |
|-------|------------|---------|-----------|--------|
| Language | Python | 3.14 | Backend runtime per NFR2 (Linux backend); consistent with U1 | NFR2 |
| BLE library | bleak | Latest stable | Python Bluetooth LE library per NFR2 (BlueZ + bleak/pygatt) | NFR2 |
| Web framework | FastAPI | Latest stable | Backend API framework per tech stack decision (Q2 feasibility) | Q2 feasibility |
| WebSocket | FastAPI WebSocket | Built-in | Real-time telemetry event streaming to frontend | Q2 feasibility |
| Testing | pytest + coverage.py | Latest | Python test framework per NFR6 | NFR6 |
| Test methodology | BDD | — | Given/When/Then scenarios per NFR8 | NFR8 |
| Coverage floor | 80% line coverage | — | Per NFR7 and team practice | NFR7 |
| CI | Tests run before merge | — | Per NFR7; failure blocks merge | NFR7 |

## Tech Stack Rationale

- **Python + bleak:** Per NFR2, the backend runs on Linux and connects to the Sphero Mini via BlueZ + a Python Bluetooth LE library. bleak is the selected library for async BLE GATT client operations (telemetry notifications/reception).
- **FastAPI:** Consistent with U1's tech stack (FastAPI backend + websockets per Q2 feasibility). U2 reuses the same FastAPI instance for telemetry event streaming via websockets.
- **pytest + coverage.py:** Per NFR6, the Python backend uses pytest for testing and coverage.py for coverage measurement. 80% line coverage floor per NFR7.
- **BDD methodology:** Per NFR8, test scenarios are written in Given/When/Then format before implementation.

## Assumptions & Open Questions

None.