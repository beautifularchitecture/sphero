# User Stories — Story Plan & Questions

## Sources

- [requirements] — requirements.md
- [team-practices] — team-practices.md
- [scope-document] — scope-document.md
- [intent-statement] — intent-statement.md

## Persona Development Approach

One primary persona: the robot operator (the user themselves, on their own machine). Goals: control the Sphero Mini via chat, observe robot state via the stats panel. No collaborators or reporting needed in this MVP. [requirements] [Q2-Intent]

## Story Format

INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable). Standard format: "As a [persona], I want [goal], so that [benefit]." Acceptance criteria in Given/When/Then (BDD) format, matching the team's affirmed BDD methodology. [team-practices]

## Story Prioritization

MoSCoW priorities assigned per story, informed by the MVP boundary. The MVP boundary is formally decided during Delivery Planning; story priorities inform that decision. [scope-document]

## Breakdown Approach

By capability instead of workflow step — movement, speed, color, stats as separate capability areas. [Q2]

## Embedded Questions

### Q1. [Product] Confirm the primary persona

- A. The robot operator (the user themselves, on their own machine, single user) — confirmed from requirements
- B. A secondary operator who monitors stats only
- C. Multiple operators with shared robot access
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. The robot operator (the user themselves, on their own machine, single user) — confirmed from requirements

### Q2. [Product] Story breakdown — confirm by workflow step

Stories broken down by the user journey: connect robot → send chat → robot moves → observe stats → handle errors.

- A. Yes — break stories down by workflow step (connect, chat, move, observe, error)
- B. Break by capability instead (movement, speed, color, stats)
- C. Break by persona (not applicable — single user)
- D. Not yet defined
- X. Other (please specify)

[Answer]: B. Break by capability instead (movement, speed, color, stats)

### Q3. [Product] MoSCoW priority for the core chat→robot story

- A. Must Have — the system is unusable without it
- B. Should Have — important but has workarounds
- C. Could Have — desirable but not essential
- D. Won't Have (this time)
- X. Other (please specify)

[Answer]: A. Must Have — the system is unusable without it

### Q4. [Product] MoSCoW priority for LED color control

- A. Must Have
- B. Should Have
- C. Could Have
- D. Won't Have (this time)
- X. Other (please specify)

[Answer]: B. Should Have — important but has workarounds

### Q5. [Product] MoSCoW priority for speed control

- A. Must Have
- B. Should Have
- C. Could Have
- D. Won't Have (this time)
- X. Other (please specify)

[Answer]: C. Could Have — desirable but not essential
