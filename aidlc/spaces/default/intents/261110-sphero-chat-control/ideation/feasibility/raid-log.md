# RAID Log — Sphero Mini Chat Control

## Risks

| ID | Risk | Likelihood | Impact | Mitigation | Source |
|----|------|------------|--------|------------|--------|
| R-01 | Bluetooth LE pairing or connection instability on Linux | Medium | High | Pair once at setup; show connection status in UI; retry with clear error | [Q1] [Q6] |
| R-02 | OpenRouter model produces unclear or unsafe robot commands | Medium | Medium | Stop robot and show error in UI on uncertainty or failure | [Q3] [Q5] |
| R-03 | Websocket connection drops between frontend and backend | Low | Medium | Reconnect on frontend; show connection status | [Q2] |
| R-04 | API key exposure if `.env` is committed | Low | High | `.env` in `.gitignore`; never commit; load at startup only | [Q4] |

## Assumptions

| ID | Assumption | Basis | Source |
|----|-----------|-------|--------|
| A-01 | Sphero Mini (original) is supported by BlueZ + bleak/pygatt on Linux | User-selected platform | [Q6] [Q1] |
| A-02 | LangChain Deep Agents package supports OpenRouter model integration | User-selected stack | [Q3] |
| A-03 | No compliance obligations for personal home-LAN project | User-selected context | [Q7] |

## Issues

| ID | Issue | Status | Source |
|----|-------|--------|--------|
| I-01 | Success metric "works reliably on the LAN" is not expressed in measurable terms | Open — user confirmed as acceptable for MVP | [Q7] |

## Dependencies

| ID | Dependency | Status | Source |
|----|-----------|--------|--------|
| D-01 | Linux machine with Bluetooth LE adapter | Required | [Q6] [Q1] |
| D-02 | OpenRouter API key | Required — user to provide in `.env` | [Q4] [Q3] |
| D-03 | Sphero Mini (original) robot, charged and pair-able | Required | [Q6] |

## Assumptions & Open Questions

None.
