# Demo Script

## Setup

1. Run `docker compose up --build`.
2. Open `http://localhost:5173`.
3. Open `http://localhost:8000/docs` if API inspection is needed.

## Walkthrough

1. Create a new session with a company name, website, and research objective.
2. Start the workflow from the session detail page.
3. Show progress events appearing as each workflow node completes.
4. Review the completed report, unknowns, and sources.
5. Ask a follow-up question grounded in the report.
6. Refresh and reopen the session from history to show persistence.

## Evaluation Notes

- Local provider mode produces deterministic output without external credentials.
- `.env` is optional; live model mode requires `MODEL_PROVIDER=openai` and `OPENAI_API_KEY`.
- Failed or attention-needed workflows can be resumed from the detail action.
