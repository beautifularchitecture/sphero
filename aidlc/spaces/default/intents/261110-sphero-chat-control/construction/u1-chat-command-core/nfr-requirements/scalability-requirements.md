# Scalability Requirements — u1-chat-command-core

Grounded in requirements [requirements], functional design [functional-spec], and rules [rules].

## Scalability Requirements

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| SCA-1 | Single user | Single user (personal MVP); no multi-user support required | N/A — no scalability NFR in inception |
| SCA-2 | Single robot | Single Sphero Mini; no multi-robot support | N/A |
| SCA-3 | Single command at a time | One chat command processed at a time; no concurrent command queuing | N/A |
| SCA-4 | Concurrency behavior | A second command arriving while one is in flight is rejected with a "busy" response; the user is prompted to retry | N/A |

## Assumptions & Open Questions

None.