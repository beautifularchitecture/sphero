# Rough Mockups — Questions

## Sources

- [desc] Initial description: "i have a sphero mini with me. it has to be able to travel based on direction input from me. so expose a local website where i can enter chat information and the sphero mini must do accordingly. the local website via websockets. Front end will be an SPA with some stats and a chat window. the stats will show direction, orientation, color, position and other paramteters... for my observaibility. requests go to the backend api which is going to be api in python again running in my local network only.. it has to use a deepagents by langchain and the model i provide initially i will use a openrouter model (i can provide the api key in .env just provide the place holder)... that shoudl translate into insturctions that the sphero mini will follow..."
- [scope] Workflow-selected scope: `mvp`.
- [Intent Q1-Q8] Intent Capture answers — intent-statement.md
- [Scope Q1-Q5] Scope Definition answers — scope-document.md, intent-backlog.md

## Q1. [Product] What are the primary user entry points and key screens/views?

This sets the screen inventory for the wireframes.

- A. One screen: chat window + stats panel side by side, no navigation
- B. Two screens: chat/robot control screen + stats dashboard screen
- C. One screen with chat at bottom, stats at top, plus an error banner
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. One screen: chat window + stats panel side by side, no navigation

## Q2. [Product] What is the core user flow (happy path)?

This defines the main interaction from opening the page to the robot moving.

- A. Open page → type chat message → agent translates → robot moves → stats update live
- B. Open page → connect robot → type chat → robot moves → stats update
- C. Open page → select command from buttons → robot moves → stats update
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. Open page → type chat message → agent translates → robot moves → stats update live

## Q3. [Product] What does the information hierarchy look like?

This decides what is most prominent on the screen.

- A. Chat window is primary (center), stats panel secondary (side rail)
- B. Stats panel is primary (top), chat input secondary (bottom)
- C. Equal split: chat and stats share the screen 50/50
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. Chat window is primary (center), stats panel secondary (side rail)

## Q4. [Product] Are there existing brand guidelines, design systems, or UI patterns to follow?

This shapes the visual design language of the SPA.

- A. None — clean, minimal, functional design for an internal tool
- B. Follow a design system (e.g., Material, Ant Design, shadcn)
- C. Brand colors and typography already chosen
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. None — clean, minimal, functional design for an internal tool

## Q5. [Product] What device/form factors must be supported?

This shapes responsive breakpoints and touch target sizing.

- A. Desktop browser only (the user's Linux machine)
- B. Desktop + tablet (LAN access from other devices)
- C. Desktop + mobile (phone access on the LAN)
- D. Not yet defined
- X. Other (please specify)

[Answer]: C. Desktop + mobile (phone access on the LAN)

## Q6. [Product] Are there known accessibility requirements?

This sets the WCAG level and keyboard/screen-reader support.

- A. WCAG 2.1 AA — keyboard navigation, color contrast, ARIA labels
- B. WCAG 2.1 A — minimum viable accessibility
- C. No formal requirement — keep it usable but don't certify
- D. Not yet defined
- X. Other (please specify)

[Answer]: C. No formal requirement — keep it usable but don't certify
