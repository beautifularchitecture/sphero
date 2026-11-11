# Functional Design Questions — u2-telemetry

Grounded in unit-of-work [unit-of-work], unit-of-work-story-map [unit-of-work-story-map], stories [stories], requirements [requirements], components [components], and contract-summary [contract-summary].

## Q1. [Engineering] Telemetry event delivery mechanism

This decides how U2 sends RobotState events to U3.

- A. Event (publish/subscribe) via websocket — U2 publishes on `robot.state.changed`, U3 subscribes
- B. Sync callback (function call) — U2 calls U3 directly on each state change
- C. Shared state store — U2 writes to a shared store, U3 polls or subscribes
- D. Not yet defined — I haven't decided the delivery mechanism
- X. Other (please specify)

[Answer]: A

## Q2. [Engineering] Telemetry polling vs event-driven

This decides how U2 receives telemetry from the Sphero Mini over Bluetooth LE.

- A. Event-driven — U2 listens for BLE notifications/indications from the robot
- B. Polling — U2 polls the robot at fixed intervals (e.g., every 1–2 seconds)
- C. Hybrid — event-driven for state changes, periodic polling for connection health
- D. Not yet defined — I haven't decided the reception mechanism
- X. Other (please specify)

[Answer]: A

## Q3. [Product] RobotState normalization and validation

This decides how U2 normalizes raw BLE telemetry into the RobotState entity.

- A. Strict validation — reject telemetry with missing/invalid fields, emit error event
- B. Lenient normalization — accept partial telemetry, fill missing fields with dashes/null, emit event anyway
- C. Hybrid — validate required fields (direction, orientation, color, position), warn on missing optional fields
- D. Not yet defined — I haven't decided the normalization approach
- X. Other (please specify)

[Answer]: B

## Q4. [Engineering] Command execution status callback from U1

This decides how U2 receives command execution status from U1 per Contract 1.

- A. Sync callback — U1 calls U2's status handler directly when a command executes
- B. Event-based — U1 publishes status events, U2 subscribes
- C. Shared state — U1 writes status to shared store, U2 reads it
- D. Not yet defined — I haven't decided the status delivery mechanism
- X. Other (please specify)

[Answer]: A

## Q5. [Product] Telemetry connection error handling

This decides what U2 does when the BLE telemetry connection drops.

- A. Stop and show error — robot stops, error published to UI, reconnect on retry
- B. Continue with last known state — emit last state with "stale" flag, retry connection in background
- C. Emit disconnected state — publish RobotState with direction=null etc., show disconnected in UI
- D. Not yet defined — I haven't decided the error handling approach
- X. Other (please specify)

[Answer]: A

## Q6. [Engineering] Bluetooth LE telemetry service/characteristic

This pins the BLE GATT service and characteristic for telemetry reception.

- A. Use the same BLE connection as U1's command sending — shared BLE client, multiplexed
- B. Separate BLE connection — dedicated GATT client for telemetry notifications
- C. Not yet defined — I haven't decided the BTE service/characteristic
- X. Other (please specify)

[Answer]: A

## Q7. [Product] Timestamp source for RobotState

This decides where the timestamp in each RobotState comes from.

- A. Robot-provided timestamp — the Sphero Mini includes a timestamp in its telemetry
- B. Backend-generated timestamp — U2 timestamps each reading when received
- C. Hybrid — prefer robot timestamp, fall back to backend timestamp
- D. Not yet defined — I haven't decided the timestamp source
- X. Other (please specify)

[Answer]: B
