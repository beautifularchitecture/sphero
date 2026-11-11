# Intent Capture & Framing — Questions

## Sources

- [desc] Initial description: "i have a sphero mini with me. it has to be able to travel based on direction input from me. so expose a local website where i can enter chat information and the sphero mini must do accordingly. the local website via websockets. Front end will be an SPA with some stats and a chat window. the stats will show direction, orientation, color, position and other paramteters... for my observaibility. requests go to the backend api which is going to be api in python again running in my local network only.. it has to use a deepagents by langchain and the model i provide initially i will use a openrouter model (i can provide the api key in .env just provide the place holder)... that shoudl translate into insturctions that the sphero mini will follow..."
- [scope] Workflow-selected scope: `mvp`.

## Q1. [Product] What problem is this solving?

Why you are building this decides what a useful first version looks like.

- A. Personal learning and tinkering with robotics plus AI agents
- B. A demo or teaching tool to show other people
- C. A foundation for a bigger product later
- D. Accessibility — an alternative way to control the robot
- E. Not yet defined
- X. Other (please specify)

[Answer]: A. Personal learning and tinkering with robotics plus AI agents

## Q2. [Product] Who uses it in this first version, and who else is involved?

Covers both the primary user and anyone who should see progress.

- A. Just me, on my own machine, no reporting needed
- B. Me plus a few people on my local network
- C. Me, with a collaborator or reviewer who looks at the docs
- D. Anyone on the LAN, no accounts
- E. Not yet defined
- X. Other (please specify)

[Answer]: A. Just me, on my own machine, no reporting needed

## Q3. [Product] Which robot capabilities must the chat drive in this first version? (select all that apply)

This sets the minimum command surface the agent must be able to produce.

- A. Directional movement: forward, back, left, right, stop
- B. Speed control
- C. Heading/orientation — turn to a stated direction
- D. LED color
- E. None of these yet / not sure
- X. Other (please specify)

[Answer]: X (A,B,C,D)

## Q4. [Product] How should the AI turn chat into robot actions?

This decides how much freedom the model has versus a fixed command vocabulary.

- A. Free-form natural language; the agent decides the commands ("roll forward a bit, then turn right")
- B. A small fixed command vocabulary the agent maps chat onto (forward/back/left/right/stop/color/speed)
- C. Both: free-form input, but the agent may only emit the fixed vocabulary
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. Free-form natural language; the agent decides the commands ("roll forward a bit, then turn right")

## Q5. [Engineering] What should happen when the agent is uncertain or something fails?

This is the fail-safe behaviour for unclear chat, a dropped robot link, or a model/API error.

- A. Stop the robot and ask me in chat before doing anything risky
- B. Stop the robot and show the error in the UI
- C. Keep the last safe motion until told otherwise
- D. Not yet defined
- X. Other (please specify)

[Answer]: B. Stop the robot and show the error in the UI

## Q6. [Engineering] Which robot model and host machine should this target?

This pins the Bluetooth library and the operating system the backend runs on.

- A. Sphero Mini (original), backend on macOS
- B. Sphero Mini (original), backend on Linux
- C. Sphero Mini 2, backend on macOS
- D. Sphero Mini 2, backend on Linux
- E. Not yet defined / I will confirm
- X. Other (please specify)

[Answer]: B. Sphero Mini (original), backend on Linux

## Q7. [Product] What does success look like, in measurable terms?

Gives the first version a pass/fail bar instead of a vague "it works".

- A. Chat message to robot motion in under about one second, with stats updating live
- B. It just works reliably on my LAN; exact latency is not critical
- C. A demo-able end-to-end run in under ten minutes
- D. Not yet defined
- X. Other (please specify)

[Answer]: B. It just works reliably on my LAN; exact latency is not critical

## Q8. [Product] What should this first version explicitly not do? (select all that apply)

The plan is already the mvp scope; this only sets the product boundary.

- A. No autonomous navigation or obstacle avoidance
- B. No multi-robot support
- C. No cloud hosting or access from outside the local network
- D. Nothing more than the above — keep it minimal
- E. Not yet defined
- X. Other (please specify)

[Answer]: A,B,C,D

## Consolidated Summary Confirmation

- Problem: Personal learning and tinkering with robotics plus AI agents [Q1]
- Users: Just me, on my own machine, no reporting needed [Q2]
- Robot capabilities: Directional movement, speed control, heading/orientation, LED color [Q3] [Q8]
- Chat-to-action: Free-form natural language; the agent decides the commands [Q4]
- Failure behaviour: Stop the robot and show the error in the UI [Q5]
- Target platform: Sphero Mini (original), backend on Linux [Q6]
- Success metric: Works reliably on the LAN; exact latency not critical [Q7]
- Out of scope: No autonomous navigation, no multi-robot, no cloud, keep it minimal [Q8]

- Looks correct
- Request changes

[Answer]: Looks correct
