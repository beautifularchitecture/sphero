# NFR Design Questions — u2-telemetry

Grounded in NFR requirements [performance-requirements, security-requirements, scalability-requirements, reliability-requirements, observability-requirements, tech-stack-decisions], functional-spec [functional-spec], and contract-summary [contract-summary].

## Q1. [Resilience] BLE reconnection and circuit breaking

NFR2.3 requires U2 to auto-reconnect within 5 seconds of a BLE telemetry connection drop, retrying up to 3 times with exponential backoff. Should U2 also trip a circuit breaker after repeated BLE failures (stopping publish attempts and degrading gracefully), or rely on retry-with-backoff alone?

- A. Retry-with-backoff only (5s reconnect, up to 3 retries, exponential backoff); no circuit breaker
- B. Add a circuit breaker that trips after N consecutive BLE failures and falls back gracefully
- C. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q2. [Performance] Event publishing path

NFR4.1 requires publishing RobotStateChanged within 500ms of BLE receipt; NFR4.2 requires sustaining up to 10 events/sec. Should U2 publish events asynchronously (queue + background publisher) so telemetry reception is never blocked by publishing, or publish synchronously on each receipt?

- A. Asynchronous publish (queue + background publisher) to keep BLE reception non-blocking
- B. Synchronous publish on each telemetry receipt (simpler, blocks briefly per event)
- C. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q3. [Security] BLE device identity validation

NFR2.1 requires BLE encryption (pairing required) for telemetry reception. Beyond pairing, should U2 validate the paired device's identity (allowlist of trusted BLE addresses) before accepting telemetry, or accept any paired device?

- A. Validate paired device identity (allowlist of trusted device addresses)
- B. Accept any paired device (encryption via pairing is sufficient)
- C. Not yet defined
- X. Other (please specify)

[Answer]: B

## Q4. [Observability] Logging and correlation for RobotStateChanged events

NFR3.1 says log only BLE connection errors and disconnections — not every RobotStateChanged event (up to 10/sec, fire-and-forget per Contract 2). How should U2 make the unlogged events traceable for observability?

- A. Emit a correlation ID per RobotStateChanged event (traceable via Contract 2 topic) but do not log each event
- B. Log every event at DEBUG level (persisted only when debug logging is enabled)
- C. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q5. [Logical components] U2 telemetry component boundary

Contract 2 names U2 as owner of the RobotStateTelemetry event. U2 receives BLE telemetry, normalizes it into RobotState, and publishes RobotStateChanged. Should U2 be a single logical component (RobotTelemetry) owning the full telemetry path, or split into separate BLE-receiver and event-publisher components?

- A. Single logical component (RobotTelemetry) owning receive → normalize → publish
- B. Split into BLE receiver component + event publisher component
- C. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q6. [Scalability] Fan-out and consumer count

NFR4.5 says U2's RobotStateChanged event supports exactly one consumer (U3 StatsDisplay) per Contract 2, with no fan-out or message bus. Confirm this single-consumer design, or should U2 design for multi-subscriber fan-out now?

- A. Confirm single-consumer design (one subscriber, U3 StatsDisplay); no fan-out infrastructure
- B. Design for multi-subscriber fan-out (message bus / broker) even though only U3 subscribes today
- C. Not yet defined
- X. Other (please specify)

[Answer]: A
