# Integration Test Instructions — sphero-chat-control

Test Strategy: **Standard** (`aidlc-state.md` → `**Test Strategy**: Standard`), so
this stage generates the integration instruction set only. Performance and
security test instruction files are not generated (Standard, not Comprehensive).

Grounded in `u2-telemetry/code-generation/code-summary.md`,
`u3-stats-ui/code-generation/code-summary.md`, the Testing Contract in each
`code-generation-plan.md` ("Unit tests plus integration tests for key
boundaries"), and Contract 2 (`/ws/robot-state`, RobotStateChanged).

## 1. Framework setup

| Boundary | Runner | Environment |
|---|---|---|
| U2 event bus → publisher → FastAPI `/ws` | pytest + pytest-asyncio | Node-free Python process, mocked BLE |
| U1 chat command → U2 command status (Contract 1) | pytest | mocked U1 callback |
| U3 WebSocket → UI render | Vitest + React Testing Library | jsdom, `global.WebSocket` replaced by `frontend/src/test-utils/mockWebSocket.ts` |
| U3 selector → chat-command callback | Vitest + React Testing Library | jsdom, callback stubbed |

No container, database, or external service is required. No real browser engine
is available in this plan; every UI integration check is a DOM-emulator
(jsdom) run and is integration evidence only.

## 2. How to run

```bash
# U2 cross-component boundaries (event bus -> publisher -> API/service)
python3 -m pytest u2_telemetry/ -v --cov=u2_telemetry --cov-report=term-missing

# U3 boundaries (WebSocket -> UI, selector -> callback)
npx vitest run --reporter=verbose \
  frontend/src/integration-websocket-to-ui.test.tsx \
  frontend/src/integration-speed-color-chat.test.tsx
```

The full U3 suite (9 files, 45 tests) is also run by Build and Test via
`npx vitest run --reporter=dot`.

## 3. Key boundaries and expected behaviour

### B1 — Raw BLE telemetry → RobotStateChanged (U2)

- `RobotState.normalizer` fills missing fields with dash/null placeholders
  (BR1.4.1, NFR4.6) and never blocks.
- `event_bus` broadcasts `robot.state.changed` to subscribers without a
  transport dependency (Contract 2).
- `event_publisher` forwards each normalized state to the WebSocket stream
  (NFR4.2 ceiling 10 events/s is a design envelope, not a timing assertion).

Expected: `u2_telemetry/tests/test_event_bus.py`, `test_event_publisher.py`,
`test_normalizer.py` and `test_service.py` pass; U2 coverage stays ≥ 80%.

### B2 — BLE drop → reconnect (U2)

- `ble_listener` retries up to 3 times with exponential backoff and reports the
  connection state (NFR2.3, NFR3.2).
- A failed connection never emits a command path and the error is surfaced
  (NFR2.2).

Expected: `test_ble_listener.py` and `test_connection_handler.py` pass.

### B3 — U1 command status → U2 correlation (U2, best-effort)

- U2 records a U1 `CommandExecutionStatus` when present and keeps publishing
  telemetry when U1 is unavailable (NFR2.4).

Expected: `test_callback_handler.py` and `test_service.py` pass.

### B4 — WebSocket telemetry → stats panel render (U3)

Given a valid RobotStateChanged frame on `/ws/robot-state`, when it arrives,
then the panel renders the values, the event counter advances and the
connection indicator shows connected. A malformed frame changes nothing and
logs no payload. A close followed by backoff shows "reconnecting (attempt 1)"
then connected (NFR3.1, NFR3.4, NFR3.5, NFR1.2).

Expected: `frontend/src/integration-websocket-to-ui.test.tsx` passes (jsdom).

**Known defect:** the hook constructs a relative URL
(`new WebSocket('/ws/robot-state')`), which throws in a real browser. The test
mocks `global.WebSocket`, so it passes without exercising a real connection.
Until Code Generation fixes the URL, B4's production path is broken and is
recorded as `Not Met` in the Target Verification Matrix.

### B5 — Speed/color selector → chat command (U3 → U1)

Given the selector with an `onSendChatCommand` callback, when the person picks a
speed or colour, then the callback receives exactly `set speed <level>` or
`set color <color>` (BR1.5.5). When no callback is supplied the buttons are
disabled.

Expected: `frontend/src/integration-speed-color-chat.test.tsx` passes (jsdom).
The shipped `App.tsx` currently passes no callback, so in the real app the
buttons stay disabled; that wiring belongs to U1's chat window.

## 4. Environment and test data

- No `.env` is needed for the suite; BLE and OpenRouter are mocked.
- RobotState payloads must match Contract 2: required `timestamp: string`;
  optional `direction`, `orientation`, `color`, `position`,
  `connectionStatus`; include missing-field and explicit-`null` cases.
- Tests must be independent and self-contained; reset the mock WebSocket
  registry between cases.
- Tests must not print telemetry payloads (NFR1.3, U3 client logging decision).

## 5. Not covered here

- Live robot / BLE round-trip (NFR4.2, NFR2.1) — needs hardware.
- LLM latency (NFR4.3, NFR4.1) — needs OpenRouter; no scheduled validation
  stage exists in this plan.
- Real-browser rendering and reconnection (NFR3.2, NFR3.3) — jsdom only.
- Load/performance and SAST/DAST — Standard strategy does not generate those
  instruction files.
