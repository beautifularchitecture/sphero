# Refined Mockups — Sphero Mini Chat Control

Grounded in wireframes [wireframes], user-flow [user-flow], stories [stories], requirements [requirements], and team-practices [team-practices].

## Design Decisions

| Decision | Value | Source |
|----------|-------|--------|
| Screen layout | One unified screen: chat + stats side by side | [Q1] [wireframes] |
| Interaction patterns | Inline speed/color selector buttons alongside chat input | [Q2] |
| Screen states | Empty, loading, error, success, partial | [Q3] |
| Design system | None — clean, minimal, functional UI | [Q4] |
| Accessibility | No formal WCAG requirement — keep usable but don't certify | [Q5] |
| Responsive breakpoints | Desktop only (the user's Linux machine) | [Q6] |

## Screen: Main Control Screen

```
+---------------------------------------------------------------------------+
| Sphero Mini Chat Control              [● Robot connected]                 |
+---------------------------------------------------------------------------+
|                                                                           |
|  CHAT WINDOW (primary)                    STATS PANEL (secondary)        |
|                                                                           |
|  +---------------------------------------+  +--------------------------+ |
|  | [User: roll forward]                  |  | ● Direction:  north      | |
|  | [Agent: MOVE_FORWARD speed=medium]    |  | ● Orientation: 90 deg    | |
|  | [Robot: moving...]                    |  | ● Color:        blue     | |
|  |                                       |  | ● Position:   (1.2, 0.4) m | |
|  | [User: set color red]                 |  |                          | |
|  | [Agent: SET_COLOR red]                |  |                          | |
|  |                                       |  |                          | |
|  | [Speed: ○ Low ● Medium ○ High]        |  |                          | |
|  | [Color: [red] [blue] [green] buttons] |  |                          | |
|  |                                       |  |                          | |
|  | +---------------------------------+   |  |                          | |
|  | | Type a message to the robot...  |   |  |                          | |
|  | +---------------------------------+   |  |                          | |
|  | [Send]                                |  |                          | |
|  +---------------------------------------+  +--------------------------+ |
|                                                                           |
+---------------------------------------------------------------------------+
```

<!-- Text fallback: Header bar with app title "Sphero Mini Chat Control" and robot connection status indicator on the right. Two panels side by side: chat window on the left (primary) with message history, speed/color inline selector buttons, message input field, and Send button; stats panel on the right (secondary) showing direction, orientation, color, position with live-updating values. -->

## Component Specifications

| Component | Type | States | Accessibility | Source |
|-----------|------|--------|---------------|--------|
| Message list | display | default, loading, empty, error | role="log", aria-live="polite" | [wireframes] |
| Message input | input | default, focused, disabled | label="Message", required | [wireframes] |
| Send button | action | default, hover, focus, disabled | type="submit", keyboard: Enter | [wireframes] |
| Speed selector | input | Low / Medium / High | aria-label="Robot speed", keyboard: arrow keys | [Q2] |
| Color selector | input | red / blue / green buttons | aria-label="LED color", keyboard: Tab/Enter | [Q2] |
| Direction stat | display | default, updating | aria-label="Robot direction" | [wireframes] |
| Orientation stat | display | default, updating | aria-label="Robot orientation" | [wireframes] |
| Color stat | display | default, updating | aria-label="LED color" | [wireframes] |
| Position stat | display | default, updating | aria-label="Robot position" | [wireframes] |
| Connection status | feedback | connected, disconnected, pairing, error | role="status", aria-live="polite" | [user-flow] |

## State Mockups

### Empty state — no robot connected yet

Header shows "● Robot disconnected" in amber. Stats panel shows dashes ("—") for all values. Chat input is enabled but a tooltip explains pairing is needed first.

### Loading state — connecting to robot

Header shows "○ Pairing…" spinner. Stats panel is disabled/greyed. Chat input disabled.

### Error state — pairing failed

Header shows "● Pairing failed" in red. Error banner in chat UI: "Could not pair with Sphero Mini. Check Bluetooth and retry." Recovery: user pairs/reconnects robot.

### Success state — connected

Header shows "● Robot connected" in green. Stats panel shows live values. Chat input enabled. Speed/color selector buttons enabled.

### Partial state — some stats missing

Stats panel shows available values; missing values show "—" with a tooltip explaining the telemetry field is not yet available.

## Assumptions & Open Questions

None.
