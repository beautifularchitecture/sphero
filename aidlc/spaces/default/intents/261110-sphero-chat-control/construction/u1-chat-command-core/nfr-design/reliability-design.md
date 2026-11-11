# Reliability Design — u1-chat-command-core

Grounded in NFR requirements [reliability-requirements], functional design [functional-spec], and contract design [contract-summary].

## NFR7 — Coverage Floor and CI

| ID | Requirement | Design | Implementation |
|----|-------------|--------|----------------|
| NFR7.1 | Line coverage floor 80% | Unit tests + integration tests for all backend components; coverage measured with coverage.py. | pytest + coverage.py; CI gate fails if coverage < 80%. |
| NFR7.2 | CI before merge | Tests run in CI before merge; failure blocks merge. | GitHub Actions workflow; run tests on push/PR; block merge on failure. |

## NFR8 — Testing Methodology

| ID | Requirement | Design | Implementation |
|----|-------------|--------|----------------|
| NFR8.1 | BDD methodology | Given/When/Then scenarios first, then implement, then run tests. | Gherkin feature files; pytest-bdd for test execution. |

## Reliability Design

- **Bluetooth retry**: Bluetooth commands retry once with backoff on failure; robot reconnects on disconnection.
- **Error handling**: All integration boundaries (API calls, Bluetooth LE, file I/O) have error handling; errors surfaced to chat UI.
- **Silent failure prevention**: No silent failures; all errors logged and surfaced to user.

## Assumptions & Open Questions

None.
