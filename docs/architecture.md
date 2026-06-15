# Architecture

## System Overview

Research Copilot has four runtime parts: React, FastAPI, LangGraph, and PostgreSQL.

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

- Routers own request and response contracts.
- Services coordinate sessions, workflow runs, reports, and chat.
- Repositories own database access.
- Integrations hide model, search, and page-fetch providers.
- Workflow modules own graph state, nodes, routing, and report generation.

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

The graph uses shared state, retries, conditional routing, intermediate outputs, and checkpointed thread IDs.

## Persistence

Application tables store sessions, workflow steps, events, reports, sources, and chat messages. LangGraph checkpoints use the session ID as `thread_id`. Tests use SQLite and an in-memory checkpointer; Docker Compose uses PostgreSQL for both application data and checkpoints.

## Progress And Recovery

Workflow events are persisted before they are shown in the browser. The stream endpoint replays existing events, so refreshes and reconnects keep context.

Recovery uses durable thread IDs, bounded retries, quality-gated routing, a resume endpoint, and degraded reports when source coverage is insufficient.

## Local Provider Mode

Default adapters return deterministic search results, source snippets, reports, and chat answers. Setting `MODEL_PROVIDER=openai` routes report and chat generation through the live model adapter and requires `OPENAI_API_KEY` at startup.
