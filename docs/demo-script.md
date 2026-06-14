# Demo Script

## Setup

1. Start the stack with `docker compose up --build`.
2. Open `http://localhost:5173`.
3. Keep backend API docs available at `http://localhost:8000/docs`.

## Walkthrough

1. Create a new session with a company name, website, and research objective.
2. Start the workflow from the session detail page.
3. Show progress events appearing as each workflow node completes.
4. Open the completed report and review every required section.
5. Ask a follow-up question and show the answer grounded in report context.
6. Refresh the page and reopen the session from history to show persistence.

## Evaluation Notes

- The local provider mode produces deterministic output for review without external credentials.
- Live providers can be enabled through `.env`.
- The architecture supports moving workflow execution to workers without changing frontend contracts.

