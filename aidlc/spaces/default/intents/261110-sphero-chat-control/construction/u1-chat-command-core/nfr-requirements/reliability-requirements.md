# Reliability Requirements — u1-chat-command-core

Grounded in requirements analysis, functional design, and business rules.

## NFR7 — Coverage Floor and CI

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR7.1 | Line coverage floor | 80% line coverage | NFR7 |
| NFR7.2 | CI before merge | Tests run in CI before merge; failure blocks merge | NFR7 |
| NFR7.3 | Bluetooth retry/reconnection | Bluetooth commands retry once with backoff on failure; robot reconnects on disconnection | NFR7 |

## NFR8 — Testing Methodology

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR8.1 | BDD methodology | Given/When/Then scenarios first, then implement, then run tests | NFR8 |

## Assumptions & Open Questions

- OpenRouter model responds within the 3-second target for NFR4.3
- LLM responsiveness is sufficient for real-time chat-to-command translation
