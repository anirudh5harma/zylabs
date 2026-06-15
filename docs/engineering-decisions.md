# Engineering Decisions

## Decision 1: LangGraph as the Workflow Runtime

The workflow uses a LangGraph `StateGraph` with meaningful nodes, shared state, conditional routing, progress events, retries, and checkpoints.

Alternatives:

- A single backend endpoint that calls a model once.
- A hand-rolled Python pipeline without graph state or checkpoints.

Tradeoff: LangGraph adds setup complexity, but it gives durable execution, recovery points, progress visibility, and inspectable intermediate outputs.

## Decision 2: PostgreSQL for Application Data and Checkpoints

PostgreSQL stores product data and LangGraph checkpoints in local and hosted environments.

Alternatives:

- SQLite-only local persistence.
- In-memory workflow state.
- Separate stores for app data and checkpoint data.

Tradeoff: PostgreSQL requires Docker or managed infrastructure, but it mirrors production behavior and survives restarts.

## Decision 3: Provider Adapters Around Model, Search, and Fetching

Workflow nodes call adapter interfaces instead of concrete providers.

Alternatives:

- Calling provider SDKs directly inside nodes.
- Hardcoding only deterministic local data.

Tradeoff: Adapters add indirection, but they keep tests deterministic and allow provider swaps without graph changes.

## Top Technical Debt Items

- Move workflow execution from the API process to workers.
- Add authentication and tenant boundaries.
- Add cost budgets, rate limits, tracing, and quality dashboards.
- Improve source deduplication and credibility scoring.
- Resolve current frontend dependency audit findings without breaking upgrades.

## Biggest Technical Risk

Report quality depends on source availability and provider reliability. The workflow mitigates this with bounded retries, unknowns, source-backed claims, and degraded reports.

## With 2 Additional Weeks

- Add queue-backed workflow execution and worker autoscaling.
- Add authenticated workspaces and row-level tenant boundaries.
- Add observability dashboards for cost, latency, retry rate, and report quality.
- Add source review, manual source pinning, and Alembic migrations.
