# Technology Stack — sphero

## Languages and Runtimes

| Layer | Language | Version / source |
|---|---|---|
| Backend + telemetry | Python | >=3.14 (`pyproject.toml:5`); CI uses 3.14 (`ci.yml:57`) |
| SPA | TypeScript | ~5.5 (`package.json:26`), strict mode, `react-jsx`, bundler resolution |
| Node | JavaScript runtime | Node 20 in CI (`ci.yml:21`) |
| Scripts | Bash | `backend.sh`, `frontend.sh` |

## Frameworks and Libraries

- **Python runtime**: FastAPI, Pydantic (models in `backend/app/models.py`), `bleak` (BLE), `uvicorn` (ASGI server, used at runtime but absent from `requirements.txt`), `langchain-openai` + `deepagents` + `openai` (lazy chat translation). Version constraints: unpinned in `requirements.txt` and `pyproject.toml`.
- **Python tests**: pytest, pytest-asyncio (`asyncio_mode = "auto"`), coverage.py with `fail_under = 80` and branch coverage.
- **Frontend runtime**: React 18.3.1, react-dom 18.3.1.
- **Frontend build**: Vite 5.4, `@vitejs/plugin-react` 4.3, PostCSS 8.4, Tailwind CSS 3.4, autoprefixer 10.4; TypeScript 5.5.
- **Frontend tests**: Vitest 1.6, `@vitest/coverage-v8` 1.6, jsdom 24, `@testing-library/react` 16, `@testing-library/jest-dom` 6.
- **CI/CD**: GitHub Actions (`ci.yml`), artifact upload v4; systemd unit `u2-telemetry.service` for U2 deployment.
- **Environment tooling**: `uv` for the standalone BLE smoke commands in the README; pip/npm for application dependencies.

## Configuration Notes

`package.json` declares scripts `dev`, `build`, `preview`, `test`, `test:u3`, `typecheck`. `pyproject.toml` declares the `u2-telemetry` console script. No ESLint, Black, Ruff or mypy configuration is present; those tools are named only in `.github/copilot-instructions.md` as planned quality checks. No formatter/linter gate runs in CI.
