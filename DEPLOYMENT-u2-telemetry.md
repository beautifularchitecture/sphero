# Deployment Notes — u2-telemetry

## Overview

U2 RobotTelemetry is a single-process Python service running on a Linux host
with a BLE radio (BlueZ). It receives raw telemetry from the Sphero Mini over
Bluetooth LE, normalizes it into a RobotState, and publishes RobotStateChanged
events on the `robot.state.changed` topic per Contract 2 (fire-and-forget) for
consumption by U3 StatsDisplay.

## Runtime requirements

- Linux host with Bluetooth enabled and BlueZ installed (`sudo apt install bluez`)
- Python 3.14+
- Python packages: `bleak`, `fastapi` (see `requirements.txt`)
- A paired Sphero Mini advertising BLE (BLE link-layer encryption per NFR2.1)

## Installation

```bash
# Install system dependencies
sudo apt update
sudo apt install -y bluez python3-pip
sudo systemctl enable --now bluetooth

# Install Python dependencies
pip install -r requirements.txt

# Install the systemd unit
sudo cp u2-telemetry.service /etc/systemd/system/u2-telemetry.service
sudo systemctl daemon-reload
sudo systemctl enable --now u2-telemetry
```

## Service management

```bash
sudo systemctl start u2-telemetry
sudo systemctl stop u2-telemetry
sudo systemctl restart u2-telemetry
sudo systemctl status u2-telemetry
journalctl -u u2-telemetry -f   # view logs (BLE connection errors only)
```

## Configuration

- **BLE address:** Set in `RobotTelemetryService(ble_address="...")` — scan with
  `bluetoothctl scan on` to discover the current Sphero Mini address (BLE
  random addresses may change).
- **No secrets:** U2 uses no API keys, tokens, or `.env` files (NFR2.2).
  OpenRouter integration is U1's responsibility (Contract 3).
- **Auto-restart:** systemd `Restart=always` with `RestartSec=5` aligns with
  NFR2.3 (reconnect within 5s, up to 3 retries, exponential backoff).

## Contracts

- Contract 1: U1 → U2 sync `CommandExecutionStatus` callback
  `{commandId, status, timestamp}` — U1 invokes `handle_command_status()`.
- Contract 2: U2 → U3 `RobotStateChanged` event on `robot.state.changed`
  (fire-and-forget, no retry) — delivered via the event bus/WebSocket.

## Observability

- Logs: BLE connection errors and disconnections only (not every event).
  Structured JSON via systemd journal → CloudWatch Logs.
- Alerts: BLE disconnected > 30s, publish latency p99 > 500ms, reconnect
  failure after 3 retries.

## Verification

Run the unit-scoped test command from the workspace root:

```bash
python3 -m pytest u2_telemetry/ -v --cov=u2_telemetry --cov-report=term-missing
```

Target: 80% line coverage floor, all tests green.
