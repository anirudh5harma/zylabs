# Architecture

## System Overview

Research Copilot is split into a React frontend, a FastAPI backend, a LangGraph workflow runtime, and PostgreSQL persistence.

```mermaid
flowchart TB
  Browser["Browser"] --> Frontend["React frontend"]
  Frontend --> Api["FastAPI API"]
  Api --> Services["Domain services"]
  Services --> Graph["LangGraph StateGraph"]
  Services --> Db[("PostgreSQL application tables")]
  Graph --> Checkpoints[("LangGraph checkpoints")]
  Graph --> Providers["Model, search, and page adapters"]
```

## Backend Boundaries

- API routers validate request/response contracts and delegate to services.
- Services coordinate domain behavior, workflow execution, and persistence.
- Repositories own database access and transactions.
- Integrations wrap external model, search, and page-fetching providers.
- Workflow modules own graph state, nodes, routing, and prompts.

## LangGraph Workflow

```mermaid
flowchart TB
  Start([START]) --> Plan["plan_research"]
  Plan --> Queries["build_search_queries"]
  Queries --> Fetch["fetch_sources"]
  Fetch --> Extract["extract_company_facts"]
  Extract --> Analyze["analyze_business_signals"]
  Analyze --> Quality{"quality_check"}
  Quality -->|pass| Report["generate_report"]
  Quality -->|gaps remain| GapResearch["targeted_gap_research"]
  GapResearch --> Extract
  Quality -->|unrecoverable| Degraded["generate_degraded_report"]
  Report --> Persist["persist_report"]
  Degraded --> Persist
  Persist --> End([END])
```

The graph stores raw research state and intermediate artifacts so progress, recovery, and report quality can be inspected.

## Persistence

Application tables store sessions, workflow events, workflow steps, reports, sources, and chat messages. LangGraph checkpoints store thread-scoped graph snapshots using the session ID as `thread_id`.

## Progress Streaming

The backend persists workflow events before streaming them to the browser through Server-Sent Events. A reconnecting browser can replay historical events and then continue with live updates.

## Recoverability

Each workflow run uses a durable thread ID, bounded retries, node-level error records, quality-gated routing, and degraded report generation for unrecoverable source failures. This preserves useful output even when some external information cannot be fetched.

