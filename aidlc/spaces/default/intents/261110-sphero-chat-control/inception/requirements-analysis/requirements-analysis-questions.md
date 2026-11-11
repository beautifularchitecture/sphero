# Requirements Analysis — Questions

## Sources

- [desc] Initial description: "i have a sphero mini with me. it has to be able to travel based on direction input from me. so expose a local website where i can enter chat information and the sphero mini must do accordingly. the local website via websockets. Front end will be an SPA with some stats and a chat window. the stats will show direction, orientation, color, position and other paramteters... for my observaibility. requests go to the backend api which is going to be api in python again running in my local network only.. it has to use a deepagents by langchain and the model i provide initially i will use a openrouter model (i can provide the api key in .env just provide the place holder)... that shoudl translate into insturctions that the sphero mini will follow..."
- [scope] Workflow-selected scope: `mvp`.
- [Q1-Q8] Intent Capture answers — intent-statement.md
- [Q1-Q5] Scope Definition answers — scope-document.md, intent-backlog.md
- [Practices Q1-Q6] Practices Discovery answers — team-practices.md
- [intent-statement] — intent-statement.md
- [scope-document] — scope-document.md
- [team-practices] — team-practices.md (Testing Posture: BDD methodology, 80% coverage floor, CI before merge, pytest+coverage.py)

## Q1. [Product] Functional — Which specific robot capabilities are in scope for this MVP?

Chat must drive robot actions. Confirm the exact command set.

- A. Movement only: forward, back, left, right, stop
- B. Movement + speed control (forward/back/left/right/stop at low/medium/high speed)
- C. Movement + speed + LED color
- D. Movement + speed + LED color + heading/orientation turn-to-direction
- E. Not yet defined
- X. Other (please specify)

[Answer]: B. Movement + speed control (forward/back/left/right/stop at low/medium/high speed)

## Q2. [Product] Functional — What should happen when the user sends an unclear or unrecognized chat message?

- A. Stop the robot, show the error in the chat UI, wait for a new message
- B. Ask the user to rephrase in chat before doing anything
- C. Ignore the message and keep the last safe state
- D. Not yet defined
- X. Other (please specify)

[Answer]: B. Ask the user to rephrase in chat before doing anything

## Q3. [Product] Non-functional — What reliability target should the chat→robot path meet?

This sets the measurable success bar beyond "works reliably on the LAN".

- A. Every chat command that parses to a valid robot action results in robot motion within about 2 seconds
- B. Robot motion starts within about 5 seconds of a valid command
- C. No specific timing target — "works reliably" is sufficient
- D. Not yet defined
- X. Other (please specify)

[Answer]: C. No specific timing target — "works reliably" is sufficient

## Q4. [Product] Non-functional — What observability data should the stats panel show, and how fresh must it be?

This is already answered as direction/orientation/color/position refreshed on every robot state change. Confirm or adjust.

- A. Direction, orientation, color, position — refreshed on every robot state change (confirmed)
- B. Direction, orientation, color, position — refreshed on a timer (e.g., every 1–2 seconds)
- C. Direction and color only, plus connection status
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. Direction, orientation, color, position — refreshed on every robot state change (confirmed)

## Q5. [Product] Accessibility — What WCAG level and keyboard support does the SPA need?

Practices affirmed no formal accessibility requirement (keep it usable but don't certify). Confirm or adjust.

- A. WCAG 2.1 AA — keyboard navigation, color contrast, ARIA labels
- B. WCAG 2.1 A — minimum viable accessibility
- C. No formal requirement — keep it usable but don't certify (confirmed)
- D. Not yet defined
- X. Other (please specify)

[Answer]: C. No formal requirement — keep it usable but don't certify (confirmed)

## Q6. [Engineering] Test tooling — What test runner and coverage tool should the Python backend use?

Practices affirmed pytest + coverage.py for the backend. Confirm or adjust.

- A. pytest + coverage.py (confirmed)
- B. unittest + coverage.py
- C. A different Python test stack
- D. Not yet defined — decide later
- X. Other (please specify)

[Answer]: A. pytest + coverage.py (confirmed)

## Q7. [Engineering] Frontend testing — What test runner should the React SPA use?

Practices deferred frontend runner selection until the stack is known. The stack is React (from scope). Suggest a choice.

- A. Vitest + React Testing Library
- B. Jest + React Testing Library
- C. Playwright (E2E only)
- D. Not yet defined — decide later
- X. Other (please specify)

[Answer]: A. Vitest + React Testing Library
