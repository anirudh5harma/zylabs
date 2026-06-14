# Research Copilot

Research Copilot helps a user prepare for a sales or business meeting by creating a company research session, running a LangGraph workflow, generating a structured briefing, and supporting follow-up chat grounded in the report.

## Stack

- Frontend: React, TypeScript, Vite
- Backend: Python, FastAPI
- Workflow: LangGraph
- Persistence: PostgreSQL for application data and workflow checkpoints
- Local runtime: Docker Compose

## Local Setup

1. Copy `.env.example` to `.env` and fill any provider keys needed for live research.
2. Start the full stack with Docker Compose.
3. Open the frontend at `http://localhost:5173`.
4. Open backend API docs at `http://localhost:8000/docs`.

```bash
docker compose up --build
```

The default local provider mode returns deterministic research output so the full product can be evaluated without external credentials. Live provider adapters can be enabled through environment variables.

## Repository Structure

```text
frontend/  React application and browser tests
backend/   FastAPI service, persistence, LangGraph workflow, and tests
docs/      Architecture, engineering decisions, product improvements, and demo script
```

## Required Documents

- `docs/architecture.md`
- `docs/engineering-decisions.md`
- `docs/product-improvements.md`
- `docs/demo-script.md`

## Core Flow

1. Create a research session with company name, website, and objective.
2. Start the workflow and watch progress events.
3. Review the generated report with sources and unknowns.
4. Ask follow-up questions using the completed report context.
5. Reopen session history and continue from persisted state.

## Development Commands

Backend:

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Frontend:

```bash
cd frontend
npm install
npm run test
npm run build
```

## Deployment

Docker Compose is the local demo runtime. For hosted deployment, run the same backend and frontend containers against managed PostgreSQL, or deploy the frontend as static assets and the backend as a container service. Keep the database URL and checkpoint URL pointed at the same managed PostgreSQL instance unless operational needs require separate stores.

