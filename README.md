# Sphero Mini Chat Control

This project is intended to let a local web app send chat instructions to a
Sphero Mini and show robot status. The planned stack is a Python/FastAPI
backend, a React SPA, LangChain Deep Agents with an OpenRouter model, and
Bluetooth LE communication through BlueZ and `bleak`.

> **Implementation status:** The application is still being designed. The
> hardware checks below test Bluetooth and direct Sphero control from Python;
> they do not test the planned web app, WebSocket, AI agent, or telemetry UI.
>
> This README was created with GitHub Copilot outside the project's AI-DLC
> workflow. The BLE connection, LED, and brief drive checks described here
> were run with the user's Sphero Mini.

## Requirements

- An original Sphero Mini, charged and awake.
- An Ubuntu/Linux computer with Bluetooth enabled and BlueZ installed.
- [`uv`](https://docs.astral.sh/uv/) to run the standalone Python checks.
- Keep the Sphero close to the computer while discovering and connecting. Close
  the Sphero phone app and disconnect any other Bluetooth client first; the
  robot may not accept a second connection.
- Use a clear, flat floor for movement tests. Do not test near stairs, edges,
  people, pets, or fragile objects.

The backend will also need a valid OpenRouter API key and outbound internet
access when the AI integration is implemented. Store the key in a project-root
`.env` file and never commit or share it. The app is intended for trusted
local-network use, not public internet exposure.

## Prepare Bluetooth on Ubuntu

Install and start BlueZ:

```bash
sudo apt update
sudo apt install bluez
sudo systemctl enable --now bluetooth
```

Confirm that Linux sees its Bluetooth controller:

```bash
bluetoothctl list
```

If no controller appears, enable Bluetooth in system settings and check whether
it is blocked:

```bash
rfkill list bluetooth
sudo rfkill unblock bluetooth
```

Wake the Sphero by shaking it. Scan for it:

```bash
bluetoothctl --timeout 20 scan on
```

Look for a name beginning with `SM-` (the device used for the successful test
advertised as `SM-D5A9`) and note its current address. BLE addresses can change,
so scan again if a later connection cannot find it. The computer's controller
address is not the robot's address.

Pairing is not necessarily required for BLE. Do not keep retrying a traditional
pair operation if the device reports that pairing is unsupported; `bleak`
connects to the Sphero as a BLE device. If a phone app or `bluetoothctl` is
connected, disconnect it before running Python checks.

## Run a BLE discovery and connection check

These commands use `uv`'s temporary environment (`--no-project`), so they do
not add dependencies to the application or modify a project manifest. Run them
from the repository root with the Sphero awake and advertising.

First scan from Python:

```bash
uv run --no-project --with bleak python - <<'PY'
import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover(timeout=15)
    for device in devices:
        print(f"{device.address}  {device.name or '(unnamed)'}  RSSI={device.rssi}")

asyncio.run(main())
PY
```

Then connect by the address printed for the Sphero and discover its GATT
services. Replace the example address with the latest scan result:

```bash
SPHERO_ADDRESS="PASTE-SPHERO-ADDRESS-HERE" uv run --no-project --with bleak python - <<'PY'
import asyncio
import os
from bleak import BleakClient

async def main():
    async with BleakClient(os.environ["SPHERO_ADDRESS"], timeout=20) as client:
        print(f"Connected: {client.is_connected}")
        for service in client.services:
            print(service.uuid)

asyncio.run(main())
PY
```

Success prints `Connected: True` and service UUIDs, then disconnects. In the
test on this computer, Python discovered `SM-D5A9`, connected, and listed the
Sphero's GATT services. A first connection attempt dropped during service
discovery; a retry succeeded.

If the Sphero is not found, wake it again, move it closer, turn off Bluetooth on
the phone temporarily, and rescan. Do not run these commands with `sudo`.

## Test the LEDs and motor control

The following checks use the `spherov2` library with `bleak`. The LED check
first sends a zero-speed drive command, then sets the body and user-body LEDs
to red. The script locates a Mini by its `SM-` name; keep it awake and
disconnect the phone app first.

```bash
uv run --no-project --with bleak --with spherov2 python - <<'PY'
from spherov2 import scanner
from spherov2.commands.drive import DriveFlags

toy = scanner.find_Mini(toy_name="SM-D5A9", timeout=25)
print(f"Found {toy.name} at {toy.address}; connecting...")
with toy:
    toy.drive_with_heading(0, 0, DriveFlags.FORWARD)
    print("Sent zero-speed stop command.")
    toy.multi_led_control.set_leds({
        toy.LEDs.BODY_RED: 255,
        toy.LEDs.BODY_GREEN: 0,
        toy.LEDs.BODY_BLUE: 0,
        toy.LEDs.USER_BODY_RED: 255,
        toy.LEDs.USER_BODY_GREEN: 0,
        toy.LEDs.USER_BODY_BLUE: 0,
    })
    print("Set body LEDs to red.")
print("Disconnected.")
PY
```

If your Sphero advertises a different `SM-` name, use that exact name in
`toy_name`. A successful run prints the stop and LED confirmations and exits
the BLE connection cleanly. The red LED command was successfully tested with
the user's Mini.

### Tested hardware details (for AI-DLC)

- Robot: original Sphero Mini.
- Name shown by the phone app: `SM-DSA9`.
- Name advertised to this Linux computer: `SM-D5A9` (prefix `SM-`).
- BLE address observed during testing: `F2:E1:BE:42:D5:A9`. This is a
  Bluetooth random address and may change; scan for the current address rather
  than hard-coding it in application behavior.
- Sphero vendor service UUID observed: `00010001-574f-4f20-5370-6865726f2121`.
- Successful BLE connection exposed Battery (`0000180f`), Generic Attribute
  (`00001801`), and Sphero vendor GATT services.
- Verified actions: discovered and connected with `bleak`; sent a zero-speed
  command; set body LEDs red; ran a brief forward command at speed 35 for 0.5
  seconds followed by stop; ran a one-minute forward command at speed 50
  followed by stop.
- A later longer movement attempt was interrupted and is not a verified
  successful test. A BLE disconnect or ended script does not guarantee motors
  stopped; confirm using the phone app or power off if needed.

For a brief, low-speed forward test, place the Sphero on the clear floor and
run this separately:

```bash
uv run --no-project --with bleak --with spherov2 python - <<'PY'
import time
from spherov2 import scanner
from spherov2.commands.drive import DriveFlags

toy = scanner.find_Mini(toy_name="SM-D5A9", timeout=30)
print(f"Found {toy.name} at {toy.address}; connecting...")
with toy:
    print("Driving forward briefly; then stopping.")
    try:
        toy.drive_with_heading(35, 0, DriveFlags.FORWARD)
        time.sleep(0.5)
    finally:
        toy.drive_with_heading(0, 0, DriveFlags.FORWARD)
        print("Stop command sent.")
print("Disconnected.")
PY
```

This sends a half-second forward command at speed 35, then sends a stop
command. It is a command-path smoke test, not a calibrated distance test; the
actual distance depends on the surface, battery, and robot orientation. A
brief command at speed 35 and a one-minute command at speed 50 were sent during
hardware checks; only use the short test above to verify basic control.

## Project verification

The recorded Python verification command for the project is:

```bash
pytest
```

The planned full backend coverage command is:

```bash
pytest tests/ --cov=backend/app --cov-report=term-missing
```

At present, the standalone Bluetooth checks above are the available
hardware-level verification. The planned app test commands should be confirmed
against the project configuration when the backend and frontend are in place.
