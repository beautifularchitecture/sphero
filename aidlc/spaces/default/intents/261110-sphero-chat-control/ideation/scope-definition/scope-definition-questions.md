# Scope Definition & Prioritization — Questions

## Sources

- [desc] Initial description: "i have a sphero mini with me. it has to be able to travel based on direction input from me. so expose a local website where i can enter chat information and the sphero mini must do accordingly. the local website via websockets. Front end will be an SPA with some stats and a chat window. the stats will show direction, orientation, color, position and other paramteters... for my observaibility. requests go to the backend api which is going to be api in python again running in my local network only.. it has to use a deepagents by langchain and the model i provide initially i will use a openrouter model (i can provide the api key in .env just provide the place holder)... that shoudl translate into insturctions that the sphero mini will follow..."
- [scope] Workflow-selected scope: `mvp`.
- [Q1-Q8] Intent Capture answers — intent-statement.md
- [Feasibility Q1-Q7] Feasibility answers — feasibility-assessment.md, constraint-register.md, raid-log.md

## Q1. [Product] What is the minimum viable scope that delivers value?

The smallest slice that lets you type a chat message and see the robot move, with stats updating.

- A. Chat → robot movement (forward/back/left/right/stop) + LED color + stats panel showing direction, orientation, color, position
- B. Chat → robot movement only; stats panel deferred
- C. Chat → robot movement + LED color + speed control; stats panel deferred
- D. Full robot control (all capabilities) + stats panel + error UI
- E. Not yet defined
- X. Other (please specify)

[Answer]: A. Chat → robot movement (forward/back/left/right/stop) + LED color + stats panel showing direction, orientation, color, position

## Q2. [Product] Which capabilities are must-have vs. nice-to-have? (select all that apply)

Use MoSCoW categories for this MVP.

- A. Must: Directional movement (forward/back/left/right/stop)
- B. Must: LED color control
- C. Must: Speed control
- D. Must: Stats panel (direction, orientation, color, position)
- E. Must: Error shown in UI on failure
- F. Nice-to-have: Heading/orientation turn-to-direction command
- G. Nice-to-have: Connection status indicator
- H. Not yet defined
- X. Other (please specify)

[Answer]: A,B,C,D,E,F,G

## Q3. [Product] What are the dependencies between capabilities?

- A. Backend → Bluetooth → robot must work before chat → backend → robot flows end-to-end
- B. Stats panel depends on robot telemetry websocket being live
- C. Agent command generation depends on the fixed robot command vocabulary being defined
- D. No strong dependencies; all can be built in parallel
- E. Not yet defined
- X. Other (please specify)

[Answer]: D. No strong dependencies; all can be built in parallel

## Q4. [Product] What is the sequencing preference?

- A. Risk-first: get Bluetooth + robot movement working before anything else
- B. Value-first: chat → robot end-to-end as fast as possible, polish stats later
- C. Dependency-first: build backend and frontend in parallel, then integrate
- D. Not yet defined
- X. Other (please specify)

[Answer]: B. Value-first: chat → robot end-to-end as fast as possible, polish stats later

## Q5. [Product] Are there hard deadlines tied to specific capabilities?

- A. No hard deadlines — build until it works reliably
- B. A specific demo or event date
- C. A weekend or two of effort, then ship what works
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. No hard deadlines — build until it works reliably

## Consolidated Summary Confirmation

- Minimum viable scope: Chat → robot movement + LED color + stats panel [Q1]
- Must-haves: Directional movement, LED color, speed control, stats panel, error in UI; Nice-to-haves: heading/orientation, connection status [Q2]
- Dependencies: No strong dependencies; all can be built in parallel [Q3]
- Sequencing: Value-first — chat → robot end-to-end first, polish stats later [Q4]
- Deadlines: No hard deadlines — build until it works reliably [Q5]

- Looks correct
- Request changes

[Answer]: Looks correct
