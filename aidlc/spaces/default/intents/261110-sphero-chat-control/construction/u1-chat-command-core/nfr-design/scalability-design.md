# Scalability Design — u1-chat-command-core

Grounded in NFR requirements [scalability-requirements], functional design [functional-spec], and contract design [contract-summary].

## NFR7 — Scalability Requirements Design

| ID | Requirement | Design | Implementation |
|----|-------------|--------|----------------|
| SCA-1 | Single user | Single-user desktop application; no multi-user support required. | No authentication or multi-tenancy; single operator per machine. |
| SCA-2 | Single robot | Single Sphero Mini; no multi-robot support required. | Single Bluetooth LE connection; one robot instance in application state. |
| SCA-3 | Single command at a time | One chat command processed at a time; no concurrent command queuing. | Sequential command processing; reject new commands while one is in flight with "busy" response. |
| SCA-4 | Concurrency behavior | Second command arriving while one is in flight is rejected with "busy" response; user prompted to retry. | Command queue with capacity 1; reject with busy status; user retries after current command completes. |

## Concurrency Model

- **Single-threaded command processing**: Chat messages processed sequentially; no concurrent command execution.
- **Command queue**: Capacity of 1; new commands while one is in flight are rejected with "busy" status.
- **User retry**: User receives "busy" message and can retry after current command completes.

## Assumptions & Open Questions

None.
