# Accessibility Checklist — Sphero Mini Chat Control

## Accessibility Decision

No formal WCAG requirement — keep usable but don't certify. [Q5]
This checklist is a best-effort baseline for usability, not a certification target.

## Perceivable

| Requirement | Status | Implementation | Source |
|-------------|--------|----------------|--------|
| Non-decorative images have alt text | N/A | No images in this UI | [Q4] |
| Color is not the sole means of conveying meaning | Partial | Status indicator uses colored dot + text label ("Robot connected") | [Q5] |
| Text contrast meets minimum ratios | Not verified | No formal WCAG target; use default browser contrast | [Q5] |
| UI components have accessible names | Partial | ARIA labels on stats values (direction, orientation, color, position) | [wireframes] |

## Operable

| Requirement | Status | Implementation | Source |
|-------------|--------|----------------|--------|
| All functionality available via keyboard | Partial | Tab into message input, Enter to send, arrow keys for speed/color selectors | [wireframes] [Q2] |
| Visible focus indicators | Not specified | No formal focus style defined; use browser defaults | [Q5] |
| Logical tab order | Yes | Header → chat → stats, following visual layout | [Q4] |
| No keyboard traps | Yes | No modal traps in this MVP (pairing modal not yet specified) | [Q4] |
| Touch targets minimum 44×44 CSS px | Not specified | Not defined for desktop-only target | [Q6] |

## Understandable

| Requirement | Status | Implementation | Source |
|-------------|--------|----------------|--------|
| Page language declared | Not specified | HTML lang attribute not yet specified | [Q4] |
| Form inputs have visible labels | Yes | Message input has label="Message" | [wireframes] |
| Error identification is specific | Yes | Error banner shows plain-language message | [user-flow] [US1.5] |
| Consistent navigation across screens | N/A | Single screen, no navigation | [Q1] |

## Robust

| Requirement | Status | Implementation | Source |
|-------------|--------|----------------|--------|
| Valid HTML semantics | Not specified | To be implemented in Code Generation | [Q4] |
| ARIA roles used correctly | Partial | role="log" on message list, role="status" on connection status | [wireframes] |
| Works across browsers | Not specified | Not tested; desktop-only target | [Q6] |

## Notes

- WCAG 2.1 AA not certified — this is a baseline checklist only. [Q5]
- Keyboard navigation covers the primary user flow (chat input + send + selectors). [Q2]
- Color is used alongside text labels for status indicators (not color alone). [Q4]

## Assumptions & Open Questions

None.
