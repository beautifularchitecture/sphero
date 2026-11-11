# Reliability Requirements — u1-chat-command-core

Grounded in requirements analysis, functional design, and business rules.

## NFR7 — Coverage Floor and CI

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR7.1 | Line coverage floor | 80% line coverage | NFR7 |
| NFR7.2 | CI before merge | Tests run in CI before merge; failure blocks merge | NFR7 |
| NFR7.3 | Bluetooth retry/reconnection | Bluetooth commands retry once with backoff on failure; robot reconnects on disconnection | NFR7 |

## NFR8 — Testing Methodology

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| NFR8.1 | BDD methodology | Given/When/Then scenarios first, then implement, then run tests | NFR8 |

## Assumptions & Open Questions

- OpenRouter model responds within the 3-second target for NFR4.3
- LLM responsiveness is sufficient for real-time chat-to-command translation

## Bluetooth LE Setup on Ubuntu

The Sphero Mini connects via Bluetooth LE. On Ubuntu, set up Bluetooth LE as follows:

### Prerequisites

1. **Verify Bluetooth hardware**: Ensure your Ubuntu machine has a Bluetooth LE (Bluetooth 4.0+) adapter:
   ```bash
   hciconfig -a
   ```
   Look for "LE" support in the output.

2. **Install BlueZ** (Linux Bluetooth stack):
   ```bash
   sudo apt update
   sudo apt install bluez bluez-tools
   ```

3. **Enable Bluetooth**:
   ```bash
   sudo systemctl enable bluetooth
   sudo systemctl start bluetooth
   ```

4. **Verify Bluetooth adapter**:
   ```bash
   hciconfig hci0 up
   hciconfig hci0
   ```
   The output should show "UP RUNNING" and the LE link type.

5. **Pair the Sphero Mini**:
   - Power on the Sphero Mini (it enters pairing mode automatically when awake)
   - Scan for devices:
     ```bash
     bluetoothctl
     scan on
     ```
   - Find the Sphero Mini in the scan results (typically appears as "Sphero-Mini-XXXX")
   - Pair and connect:
     ```bash
     pair <MAC_ADDRESS>
     connect <MAC_ADDRESS>
     trust <MAC_ADDRESS>
     ```
   - Exit bluetoothctl:
     ```bash
     exit
     ```

6. **Verify connection**:
   ```bash
   bluetoothctl info <MAC_ADDRESS>
   ```
   Should show "Connected: yes".

### Important Notes

- The Sphero Mini enters pairing mode when awakened (shake it or press the button)
- Pairing is required once; subsequent connections are automatic when the robot is awake
- If pairing fails, ensure the Sphero Mini is charged and in pairing mode
- The backend Python application (using `bleak` or `pygatt`) connects to the paired device via its MAC address
