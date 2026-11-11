# Design System Mapping — Sphero Mini Chat Control

## Design System Decision

No formal design system. Clean, minimal, functional UI — confirmed from rough mockups Q4. [Q4]

## Design Tokens

| Token | Value | Usage | Source |
|-------|-------|-------|--------|
| Color — primary | #2563eb (blue) | Primary actions, Send button, connected status | [Q4] |
| Color — success | #16a34a (green) | Robot connected indicator, success states | [Q4] |
| Color — warning | #d97706 (amber) | Pairing in progress, partial stats | [Q4] |
| Color — error | #dc2626 (red) | Disconnected, errors, stop state | [Q4] |
| Color — neutral text | #1f2937 (dark gray) | Body text, labels | [Q4] |
| Color — neutral bg | #ffffff (white) | Page background | [Q4] |
| Spacing — unit | 8px | Base spacing unit for margins/padding | [Q4] |
| Typography — heading | System sans-serif, bold | App title, section headings | [Q4] |
| Typography — body | System sans-serif, regular | Chat messages, stats labels | [Q4] |

## Component Mapping

| Component | Design System Equivalent | Notes |
|-----------|-------------------------|-------|
| Message list | — | Custom scrollable log, no design system equivalent |
| Message input | — | Standard text input with label |
| Send button | Primary button | Filled blue, white text |
| Speed selector | Segmented control / toggle group | Three mutually exclusive buttons |
| Color selector | Segmented control / toggle group | Three mutually exclusive color buttons |
| Stats panel | Card | Bordered container with labeled value rows |
| Connection status | Badge / status indicator | Colored dot + text label |
| Error banner | Alert | Red background, dismissible |

## Responsive Behavior

Desktop only — the user's Linux machine is the target device. [Q6]
No tablet or mobile breakpoints needed for this MVP.

Layout:
- Header: full width, flex row with title left and status right
- Main area: two panels side by side (chat ~60%, stats ~40%)
- On smaller desktop windows: panels stack vertically (chat on top, stats below)

## Assumptions & Open Questions

None.
