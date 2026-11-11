# Team Allocation — Sphero Mini Chat Control

Grounded in unit-of-work [unit-of-work], unit-of-work-dependency [unit-of-work-dependency], and team-practices [team-practices].

## Mob Allocation

Practices-discovery was run (scope: mvp) and the collaborators switch was off, so Team Formation (stage 1.5) did not run. Per the Delivery Planning stage contract, when 1.5 is SKIP (mvp, classic), all Bolts are executed by aidlc-developer-agent (AI) as a solo mob.

| Bolt | Unit(s) | Mob | Owner |
|------|---------|-----|-------|
| Bolt 1 | U1 (u1-chat-command-core) | aidlc-developer-agent (AI, solo) | aidlc-developer-agent |
| Bolt 2 | U2 (u2-telemetry) | aidlc-developer-agent (AI, solo) | aidlc-developer-agent |
| Bolt 3 | U3 (u3-stats-ui) | aidlc-developer-agent (AI, solo) | aidlc-developer-agent |

## Roles (within the solo mob)

The aidlc-developer-agent performs all mob roles for each Bolt:
- **Driver**: writes the code
- **Navigator**: reviews the code as it is written
- **Researcher**: looks up Bluetooth LE, OpenRouter, LangChain Deep Agents, FastAPI, React details as needed

## Communication Norms

- Single developer (AI); no human team members in this MVP
- Branch strategy: trunk-based on `main`, short-lived feature branches squash-merged into `main` (affirmed at practices-discovery Q1)
- Each Bolt completes on its own branch, then squash-merges to `main`
- Quality gates: linter + tests run in CI before merge; failure blocks merge (affirmed at practices-discovery Q5)
- Deployment: continuous deployment to production on every merge (affirmed at practices-discovery Q4); human approval not required for each Bolt

## Assumptions & Open Questions

- No human collaborators in this MVP; all work performed by aidlc-developer-agent
- If a human collaborator joins later, this allocation should be revisited and a Program Board created
