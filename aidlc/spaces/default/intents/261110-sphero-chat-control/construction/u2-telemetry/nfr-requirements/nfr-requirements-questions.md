# NFR Requirements Questions — u2-telemetry

Grounded in functional-spec [functional-spec], rules [rules], requirements [requirements], and contract-summary [contract-summary].

## Q1. [Engineering] Telemetry event publishing latency target

This sets the performance requirement for U2's RobotStateChanged event publishing.

- A. Publish within 500ms of receiving raw BLE telemetry
- B. Publish within 1 second of receiving raw BLE telemetry
- C. No specific target; publish as soon as possible after receipt
- D. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q2. [Engineering] Telemetry reconnection behavior

This sets the reliability requirement for U2 when the BLE telemetry connection drops.

- A. Reconnect automatically within 5 seconds, retry up to 3 times with exponential backoff
- B. Reconnect automatically within 10 seconds, retry indefinitely until successful
- C. Do not auto-reconnect; require manual re-pairing via U1 chat UI
- D. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q3. [Security] Bluetooth LE connection security

This sets the security requirement for U2's BLE telemetry reception.

- A. Use BLE encryption (pairing required) for telemetry reception
- B. No encryption; telemetry is not sensitive data
- C. Use BLE signing but not encryption
- D. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q4. [Observability] Telemetry event logging

This sets the observability requirement for U2's telemetry event publishing.

- A. Log every RobotStateChanged event with full payload to application log
- B. Log only state changes that differ from the previous state (deduplication)
- C. Log only errors and connection state changes, not every telemetry event
- D. Not yet defined
- X. Other (please specify)

[Answer]: C

## Q5. [Reliability] Graceful degradation when U1 is unavailable

This sets the reliability requirement when U1's CommandExecutionStatus callback is unavailable.

- A. U2 continues publishing telemetry; command status correlation is best-effort
- B. U2 stops publishing telemetry until U1 callback is available
- C. U2 queues telemetry events and replays them when U1 is available
- D. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q6. [Performance] Maximum telemetry event rate

This sets the performance requirement for U2's event publishing throughput.

- A. Up to 10 RobotStateChanged events per second
- B. Up to 1 RobotStateChanged event per second
- C. Up to 1 RobotStateChanged event per 5 seconds
- D. Not yet defined
- X. Other (please specify)

[Answer]: A

## Q7. [Security] API key and secret handling

This sets the security requirement for any secrets U2 might use.

- A. No secrets used by U2 (no OpenRouter, no API keys)
- B. U2 reads OpenRouter API key from .env (shared with U1)
- C. U2 uses its own secrets file outside the project tree
- D. Not yet defined
- X. Other (please specify)

[Answer]: A
