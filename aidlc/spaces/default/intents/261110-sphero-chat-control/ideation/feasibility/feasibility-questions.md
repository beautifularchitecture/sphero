# Feasibility & Constraints — Questions

## Sources

- [desc] Initial description: "i have a sphero mini with me. it has to be able to travel based on direction input from me. so expose a local website where i can enter chat information and the sphero mini must do accordingly. the local website via websockets. Front end will be an SPA with some stats and a chat window. the stats will show direction, orientation, color, position and other paramteters... for my observaibility. requests go to the backend api which is going to be api in python again running in my local network only.. it has to use a deepagents by langchain and the model i provide initially i will use a openrouter model (i can provide the api key in .env just provide the place holder)... that shoudl translate into insturctions that the sphero mini will follow..." [desc]
- [scope] Workflow-selected scope: `mvp`
- [intent-statement] — intent-statement.md

## Q1. [Engineering] How will the Python backend connect to the Sphero Mini?

This pins the Bluetooth library and any pairing requirements on your Linux machine.

- A. BlueZ + a Python Bluetooth LE library (e.g., bleak, pygatt), pairing handled once at setup
- B. Sphero's official Python SDK if it supports Mini on Linux
- C. A USB Bluetooth dongle with its own vendor tools
- D. Not yet defined — I haven't decided the connection method
- X. Other (please specify)

[Answer]: A. BlueZ + a Python Bluetooth LE library (e.g., bleak, pygatt), pairing handled once at setup

## Q2. [Engineering] Which Python tech stack for the backend and frontend?

This decides the web framework, websocket library, and SPA approach.

- A. FastAPI backend + websockets, React SPA frontend
- B. Flask backend + websockets, vanilla JS/HTML SPA frontend
- C. Python stdlib HTTP server + websockets, vanilla JS/HTML SPA frontend
- D. Not yet defined — I haven't decided the stack
- X. Other (please specify)

[Answer]: A. FastAPI backend + websockets, React SPA frontend

## Q3. [Engineering] Which LangChain Deep Agents setup and OpenRouter model?

This decides the agent framework and model invocation path for turning chat into robot commands.

- A. LangChain + LangGraph agent with OpenRouter chat model, function calling to emit commands
- B. LangChain Deep Agents package directly, OpenRouter model behind it
- C. A simpler LangChain chain (no Deep Agents), OpenRouter model
- D. Not yet defined — I'll confirm after researching the packages
- X. Other (please specify)

[Answer]: B. LangChain Deep Agents package directly, OpenRouter model behind it

## Q4. [Engineering] How is the OpenRouter API key managed?

You said you can provide it in .env. Confirm the approach.

- A. .env file at project root, loaded at backend startup, never committed
- B. Environment variable set in the shell before starting the backend
- C. A secrets file outside the project tree, read at startup
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. .env file at project root, loaded at backend startup, never committed

## Q5. [Product] What does the SPA stats panel show, and how often does it update?

This sets the observability surface the backend must expose over websockets.

- A. Direction, orientation, color, position — refreshed on every robot state change
- B. Direction, orientation, color, position — refreshed on a timer (e.g., every 1–2 seconds)
- C. Direction and color only, plus a connection status light
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. Direction, orientation, color, position — refreshed on every robot state change

## Q6. [Product] Any budget or timeline constraints?

This shapes how much time goes into the agent, frontend polish, and testing.

- A. No hard constraints — build it until it works reliably
- B. A weekend or two of effort, then ship what works
- C. A specific date or event (demo, teaching session) to be ready for
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. No hard constraints — build it until it works reliably

## Q7. [Engineering] Are there any regulatory, compliance, or organizational constraints?

This covers anything that would limit what you can build or how data flows on your LAN.

- A. None — personal project, home LAN, no compliance obligations
- B. Network policy restricts new listening services or Bluetooth on this machine
- C. Data residency or privacy rules apply to chat or robot telemetry
- D. Not yet defined
- X. Other (please specify)

[Answer]: A. None — personal project, home LAN, no compliance obligations