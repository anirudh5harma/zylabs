# Research Copilot

Research Copilot creates sales meeting briefings from a company, website, and objective. It runs a LangGraph workflow, saves the session, report, sources, workflow events, and chat history, then supports follow-up questions once the report is ready.

## Stack

- Frontend: React, TypeScript, Vite
- Backend: FastAPI, SQLAlchemy, Pydantic
- Workflow: LangGraph `StateGraph`
- Storage: PostgreSQL for application data and LangGraph checkpoints
- Runtime: Docker Compose

## Quick Start

```bash
docker compose up --build
```

- Frontend: `http://localhost:5173`
- Backend docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

The default provider mode is deterministic, so the full flow runs without external credentials. Copy `.env.example` to `.env` only when adding local overrides.

To use live model responses, set `MODEL_PROVIDER=openai` and `OPENAI_API_KEY`. Startup fails with a clear config error if live mode is enabled without a key.

## Deployment

Use Docker Compose for local demos and evaluation. For hosted deployment, run the same frontend and backend containers on a container platform with managed PostgreSQL. Keep `DATABASE_URL` and `LANGGRAPH_CHECKPOINT_URL` pointed at PostgreSQL unless there is a clear operational reason to split stores.

## Core Flow

1. Create a session with company name, website, and objective.
2. Start or resume the workflow and watch persisted progress events.
3. Review the structured report, unknowns, and sources.
4. Ask follow-up questions grounded in the completed report.
5. Reopen session history from persisted state.

## Development

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
ruff check app tests
pytest
```

```bash
cd frontend
npm install
npm run test
npm run build
```

## Structure

```text
backend/   FastAPI service, persistence, workflow, tests
frontend/  React application, API client, tests
docs/      Required architecture and product documents
```

## Docs

- `docs/architecture.md`
- `docs/engineering-decisions.md`
- `docs/product-improvements.md`
- `docs/demo-script.md`

## API

- `GET /api/v1/health`
- `POST /api/v1/sessions`
- `GET /api/v1/sessions`
- `GET /api/v1/sessions/{session_id}`
- `POST /api/v1/sessions/{session_id}/workflow/start`
- `POST /api/v1/sessions/{session_id}/workflow/resume`
- `GET /api/v1/sessions/{session_id}/workflow/events`
- `GET /api/v1/sessions/{session_id}/workflow/stream`
- `GET /api/v1/sessions/{session_id}/chat`
- `POST /api/v1/sessions/{session_id}/chat`
