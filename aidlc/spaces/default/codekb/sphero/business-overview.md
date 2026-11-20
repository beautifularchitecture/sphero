# Business Overview — sphero

## Purpose

Local web app that lets an operator send natural-language chat instructions to an original Sphero Mini and see normalized robot status/telemetry back in a browser. The intended deployment is a trusted local network, not the public internet.

## Business Domain

Robot teleoperation with a natural-language command boundary. Commands are constrained to a small vocabulary (forward/back/left/right/stop/setSpeed/setColor); unclear input or a robot failure triggers a safety stop and an error shown in the chat UI. Security and LAN-risk context is described in `code-quality-assessment.md`; component ownership in `component-inventory.md`.

## Key Functionality

- **Chat command (U1)**: validate free-form chat text, translate it to one robot command via an LLM, write it over BLE, and ack or surface a typed error.
- **Telemetry (U2)**: receive BLE notifications, normalize them leniently into `RobotState`, and publish `robot.state.changed` events.
- **Stats UI (U3)**: display connection state and telemetry fields, speed/color buttons, event counter, and an always-visible LAN-risk banner.
- **Hardware checks (documented)**: BLE discovery, LED and brief drive smoke tests recorded in the root README.

## Users and Operating Model

One local operator with a Sphero Mini, an Ubuntu/Linux host with BlueZ, and a browser. Start the backends with the root `backend.sh`, then the SPA with `frontend.sh`. An OpenRouter API key is required for chat translation. Full U2 deployment/service detail is in the root deployment notes.

## Implementation Status

All three units are implemented with test suites and CI gates. The root README still describes the app as "still being designed" and documents only the hardware-level checks — the gap this intent addresses. See `developer-scan.md` (handoff) for line-level evidence.
