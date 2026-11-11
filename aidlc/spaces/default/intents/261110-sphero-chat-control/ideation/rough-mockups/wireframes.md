# Rough Wireframes — Sphero Mini Chat Control

## Screen Inventory

One screen only, no navigation:

| Screen | Purpose | Source |
|--------|---------|--------|
| Main control screen | Chat input + stats panel side by side | [Q1] [Q3] [intent-statement] [scope-document] [intent-backlog] |

## Main Control Screen — Layout

```
+---------------------------------------------------------------------------+
| Sphero Mini Chat Control              [Robot status: disconnected]        |
+---------------------------------------------------------------------------+
|                                                                           |
|  CHAT WINDOW (primary)                    STATS PANEL (secondary)        |
|                                                                           |
|  +---------------------------------------+  +--------------------------+ |
|  | [User: roll forward]                  |  | Direction:  north          | |
|  | [Agent: MOVE_FORWARD speed=0.5]       |  | Orientation: 90 deg        | |
|  | [Robot: moving...]                    |  | Color:        blue         | |
|  |                                       |  | Position:   (0.0, 0.0) m   | |
|  | [User: turn right]                    |  |                           | |
|  | [Agent: TURN_RIGHT angle=90]          |  |                           | |
|  |                                       |  |                           | |
|  | +---------------------------------+   |  |                           | |
|  | | Type a message to the robot...  |   |  |                           | |
|  | +---------------------------------+   |  |                           | |
|  | [Send]                                |  |                           | |
|  +---------------------------------------+  +--------------------------+ |
|                                                                           |
+---------------------------------------------------------------------------+
```

<!-- Text fallback: Single-screen layout with a header bar at top showing the app title and robot connection status. Below, two panels side by side: a chat window on the left (primary) and a stats panel on the right (secondary) showing direction, orientation, color, and position. -->

## Chat Window — Components

| Component | Type | States | Accessibility |
|-----------|------|--------|---------------|
| Message list | display | default, loading, empty, error | role="log", aria-live="polite" |
| Message input | input | default, focused, disabled | label="Message", required |
| Send button | action | default, hover, focus, disabled | type="submit", keyboard: Enter |

## Stats Panel — Components

| Component | Type | States | Accessibility |
|-----------|------|--------|---------------|
| Direction | display | default, updating | aria-label="Robot direction" |
| Orientation | display | default, updating | aria-label="Robot orientation" |
| Color | display | default, updating | aria-label="LED color" |
| Position | display | default, updating | aria-label="Robot position" |
| Robot status | feedback | connected, disconnected, error | role="status", aria-live="polite" |

## Accessibility Notes (per screen)

| Screen | Heading level | Primary landmark | Keyboard entry point |
|--------|--------------|------------------|----------------------|
| Main control screen | h1 | main | Message input field |

- WCAG: No formal requirement — keep it usable but don't certify [Q6]
- Device support: Desktop + mobile [Q5]
- Visual design: Clean, minimal, functional — no design system [Q4]

## Assumptions & Open Questions

None.
