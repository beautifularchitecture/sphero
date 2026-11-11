# Refined Mockups — Questions

## Sources

- [wireframes] — rough-mockups/wireframes.md
- [user-flow] — rough-mockups/user-flow.md
- [stories] — user-stories/stories.md
- [requirements] — requirements-analysis/requirements.md
- [team-practices] — practices-discovery/team-practices.md

## Q1. [Product] How should each user story be represented in the UI?

Which stories get dedicated screen space vs. shared UI elements?

- A. One unified screen: chat + stats side by side, all stories share the same UI (matches rough wireframes)
- B. Two screens: a robot control screen (chat + movement/color/speed controls) and a separate stats dashboard
- C. Chat-first screen with stats as a collapsible side panel that can be hidden
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. One unified screen: chat + stats side by side, all stories share the same UI (matches rough wireframes)

## Q2. [Product] What interaction patterns are needed?

Which patterns should the refined mockups specify beyond basic chat input?

- A. Modal for robot pairing/connection setup (first-time use)
- B. Inline speed/color selector buttons alongside chat input
- C. Progressive disclosure: advanced robot settings hidden behind an "options" toggle
- D. None — keep it minimal: chat input + stats display only
- E. Not yet defined
- X. Other (please specify)

[Answer]: B. Inline speed/color selector buttons alongside chat input

## Q3. [Product] What states must each screen handle?

Beyond the happy path, which screen states need explicit mockups?

- A. Empty state (no robot connected yet), loading state (connecting), error state (pairing failed), success state (connected), partial state (some stats missing)
- B. Only happy path + error state — keep it minimal
- C. Empty + loading + error — skip success and partial states
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. Empty state (no robot connected yet), loading state (connecting), error state (pairing failed), success state (connected), partial state (some stats missing)

## Q4. [Product] Does the design align with an existing design system / component library?

This project affirmed no formal design system (clean, minimal, functional). Confirm or adjust.

- A. No design system — clean, minimal, functional UI (confirmed from rough mockups Q4)
- B. Use a component library (e.g., shadcn, Material UI) for consistent components
- C. Custom design tokens (colors, spacing, typography) defined for this project
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. No design system — clean, minimal, functional UI (confirmed from rough mockups Q4)

## Q5. [Product] What accessibility requirements apply?

Practices affirmed no formal WCAG requirement (keep usable but don't certify). Confirm or adjust.

- A. No formal WCAG requirement — keep usable but don't certify (confirmed)
- B. WCAG 2.1 AA — keyboard navigation, color contrast, ARIA labels
- C. WCAG 2.1 A — minimum viable accessibility
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. No formal WCAG requirement — keep usable but don't certify (confirmed)

## Q6. [Product] What responsive breakpoints are needed?

Rough mockups affirmed desktop + mobile support. Confirm the breakpoint strategy.

- A. Mobile-first: mobile (<768px), tablet (768–1023px), desktop (>1024px)
- B. Desktop only — the user's Linux machine is the target device
- C. Mobile + desktop only (skip tablet)
- D. Not yet defined
- X. Other (please specify)

[Answer]: B. Desktop only — the user's Linux machine is the target device
