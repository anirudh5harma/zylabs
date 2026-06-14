# Engineering Decisions

## Decision 1: LangGraph as the Workflow Runtime

The research process is implemented as a LangGraph `StateGraph` with meaningful nodes, shared state, conditional routing, progress events, and checkpoints.

Alternatives considered:

- A single backend endpoint that calls a model once.
- A hand-rolled Python pipeline without graph state or checkpoints.

Tradeoffs:

- LangGraph adds setup complexity, but it gives durable execution, progress streaming, recovery points, and inspectable intermediate outputs.

## Decision 2: PostgreSQL for Application Data and Checkpoints

PostgreSQL stores both product data and LangGraph checkpoints for the local demo and hosted deployment path.

Alternatives considered:

- SQLite-only local persistence.
- In-memory workflow state.
- Separate stores for app data and checkpoint data.

Tradeoffs:

- PostgreSQL requires Docker or managed infrastructure, but it mirrors production behavior and keeps persistence durable across restarts.

## Decision 3: Provider Adapters Around Model, Search, and Fetching

Workflow nodes call adapter interfaces instead of concrete providers.

Alternatives considered:

- Calling provider SDKs directly inside nodes.
- Hardcoding only deterministic local data.

Tradeoffs:

- Adapters add indirection, but they keep tests deterministic and let live providers be swapped without changing graph logic.

## Top Technical Debt Items

- Move workflow execution from in-process background tasks to a dedicated worker once concurrency requirements are known.
- Add authentication and tenant boundaries before handling real customer data.
- Add provider-level cost budgets, rate limits, and tracing dashboards.
- Add richer source deduplication and credibility scoring.

## Biggest Technical Risk

Report quality depends on source availability and provider reliability. The workflow mitigates this with bounded retries, unknowns, source-backed claims, and degraded reports.

## With 2 Additional Weeks

- Add queue-backed workflow execution and worker autoscaling.
- Add authenticated workspaces and row-level tenant boundaries.
- Add observability dashboards for cost, latency, retry rate, and report quality.
- Add browser-based source review and manual source pinning.

