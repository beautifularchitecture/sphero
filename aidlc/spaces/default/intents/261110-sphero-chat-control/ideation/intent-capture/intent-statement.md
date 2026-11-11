# Intent Statement — Sphero Mini Chat Control

## Problem Statement

The user wants to control a Sphero Mini robot by typing chat messages into a local website, with the robot translating those messages into movement and other actions. The website runs on the local network only, and chat input goes to a Python backend that uses LangChain Deep Agents with an OpenRouter model to turn natural language into robot instructions. [desc] [Q1]

## Target Customer

The user themselves, on their own machine, with no reporting or collaborators needed in this first version. [Q2]

## Success Metrics

The system works reliably on the local area network; exact latency is not a critical target for this first version. [Q7]

## Initiative Trigger

Personal learning and tinkering with robotics plus AI agents — a hands-on project to connect chat, an AI agent, and a physical robot. [Q1]

## Initial Scope Signal

Workflow-selected scope: `mvp`. [scope]

Product boundary for this first version: no autonomous navigation or obstacle avoidance, no multi-robot support, no cloud hosting or access from outside the local network — keep it minimal. [Q8]

## Robot capabilities in scope

The chat must drive: directional movement (forward, back, left, right, stop), speed control, heading/orientation, and LED color. [Q3] [Q8]

## How chat becomes robot action

The AI turns free-form natural language chat into robot instructions — the agent decides the commands from the user's words rather than mapping onto a fixed vocabulary. [Q4]

## Failure behaviour

When the agent is uncertain or something fails, the robot stops and the error is shown in the UI. [Q5]

## Target platform

Sphero Mini (original), with the Python backend running on Linux. [Q6]

## Assumptions & Open Questions

None.
