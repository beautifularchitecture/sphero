# Tech Stack Decisions — u1-chat-command-core

Grounded in requirements analysis, scope definition, and feasibility analysis.

## Backend

| Decision | Choice | Justification | Source |
|----------|--------|---------------|--------|
| Language | Python 3.11 | User-selected stack; Linux backend | Q6-Intent |
| Web framework | FastAPI | Async web framework with native websocket support | Q2-Feas |
| WebSocket | FastAPI WebSocket | Real-time chat input from SPA frontend | Q2-Feas |
| AI agent | LangChain Deep Agents | User-selected agent framework | Q3-Feas |
| LLM model | OpenRouter chat model | User-selected model provider | Q3-Feas |
| Bluetooth LE | bleak | Python Bluetooth LE library for Sphero Mini on Linux; selected over pygatt for better asyncio support | Q1-Feas |
| Testing | pytest + coverage.py | Python test runner and coverage tool | Q6 |

## Frontend

| Decision | Choice | Justification | Source |
|----------|--------|---------------|--------|
| Framework | React | User-selected SPA frontend | Q2-Feas |
| Language | TypeScript | Type-safe frontend development | Code style |
| Build tool | Vite | Fast build and dev server | Code style |
| Testing | Vitest + React Testing Library | User-selected frontend test runner | Q7 |

## Configuration

| Decision | Choice | Justification | Source |
|----------|--------|---------------|--------|
| Environment variables | `.env` at project root | OpenRouter API key and configuration | Q4-Feas |
| `.gitignore` | Excludes `.env` and `.env.*` | Secret never committed | Q6, C-04 |

## NFR6 — Test Tooling

| ID | Requirement | Target | Source |
|----|-------------|--------|--------|
| Python test runner | pytest + coverage.py for Python backend testing | Q6 |
| Frontend test runner | Vitest + React Testing Library for React SPA testing | Q7 |

## Assumptions & Open Questions

None.
