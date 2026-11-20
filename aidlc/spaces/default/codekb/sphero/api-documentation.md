# API Documentation — sphero

## External HTTP / WebSocket Surfaces

| Interface | Location | Contract |
|---|---|---|
| `GET /health` | `backend/app/main.py:215` | `{"status":"ok","service":"u1-chat-command-core"}`; no auth, no dependency checks |
| `GET /` | `backend/app/main.py:223` | Built SPA `dist/index.html`, else 404 with guidance to run `npm run build` |
| `/assets` | `backend/app/main.py:227-229` | Static mount when `dist/assets` exists |
| `WS /ws/chat` | `backend/app/main.py:219` | One text frame in, one frame out; one-shot socket per command |
| `WS /ws/robot-state` | `u2_telemetry/api.py:49` | Subscribes to the shared bus; broadcasts `robot.state.changed` frames |

### Chat request / response

- **Request**: `{"text": "roll forward"}` (plain text frames also accepted by `_parse_chat_frame`, `backend/app/main.py:114-122`).
- **Ack**: `{"type":"ack","message":...,"commandId":...,"status":"moving|stopped","timestamp":...}` (`main.py:173-179`).
- **Error**: `{"type":"error","errorType":"validation|agent_error|bluetooth|...","message":...,"timestamp":...}` (`main.py:125-133`). Validation errors issue no BLE stop; agent/BLE/unexpected errors do (`main.py:180-203`).
- **Auth/rate limiting**: none. LAN-only design is explicitly acknowledged in `frontend/src/constants.ts:15`.

### Telemetry frame

`{"topic":"robot.state.changed","state":{"stateId":...,"correlation_id":...,"direction":...,"orientation":...,"color":...,"position":...,"timestamp":...}}` — produced by `u2_telemetry/event_bus.py:52,65-75`; shape-validated in `frontend/src/hooks/useRobotStateConnection.ts:44-88`. Delivery is fire-and-forget; no retry.

## Internal Contracts

- **Contract 1 (U1 → U2)**: sync callback `handle_command_status(command_id, status, timestamp)` carrying `CommandExecutionStatus {commandId, status, timestamp}` (`u2_telemetry/service.py:86`, `backend/app/models.py:133`). U1's default is a documented no-op (`backend/app/main.py:38-44`); live U2 wiring is deferred.
- **Contract 2 (U2 → U3)**: `robot.state.changed` event on one shared `RobotStateEventBus` instance (`u2_telemetry/__main__.py:63-77`, `api.py:35-46`).

## Device / Transport Boundaries

- U1 control write: `write_gatt_char(characteristic, payload, response=True)` with compact JSON `{commandId, command, speed?, color?}` (`backend/app/robot_command.py:99-105,113-123`); default service/characteristic UUIDs in `backend/app/config.py:25-26`.
- U2 telemetry notification: subscribes to characteristic `0000ffe1-0000-1000-8000-00805f9b34fb`, parses UTF-8 JSON leniently (`u2_telemetry/ble_listener.py:18,115-124`).
- Vite dev proxies: `/ws/chat → ws://127.0.0.1:8000`, `/ws/robot-state → ws://127.0.0.1:8001` (`vite.config.ts:12-16`).

No OpenAPI/AsyncAPI spec files were found; contracts live in code, docstrings and the root deployment notes. There is no rate limiting or authentication on any surface.
