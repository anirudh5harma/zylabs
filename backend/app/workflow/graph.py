from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy

from app.core.config import Settings
from app.integrations.model_client import LocalModelClient
from app.integrations.page_fetcher import LocalPageFetcher
from app.integrations.search_client import LocalSearchClient
from app.workflow.nodes.research import ResearchNodes
from app.workflow.routing import route_quality
from app.workflow.state import ResearchState


async def build_checkpointer(settings: Settings) -> tuple[Any | None, Any]:
    if settings.langgraph_checkpoint_url and settings.langgraph_checkpoint_url.startswith("postgresql"):
        context = AsyncPostgresSaver.from_conn_string(settings.langgraph_checkpoint_url)
        checkpointer = await context.__aenter__()
        await checkpointer.setup()
        return context, checkpointer
    return None, InMemorySaver()


def build_research_graph(checkpointer: Any | None = None):
    nodes = ResearchNodes(LocalSearchClient(), LocalPageFetcher(), LocalModelClient())
    builder = StateGraph(ResearchState)
    retry = RetryPolicy(max_attempts=2)
    builder.add_node("plan_research", nodes.plan_research, retry_policy=retry)
    builder.add_node("build_search_queries", nodes.build_search_queries, retry_policy=retry)
    builder.add_node("fetch_sources", nodes.fetch_sources, retry_policy=retry)
    builder.add_node("extract_company_facts", nodes.extract_company_facts, retry_policy=retry)
    builder.add_node("analyze_business_signals", nodes.analyze_business_signals, retry_policy=retry)
    builder.add_node("quality_check", nodes.quality_check, retry_policy=retry)
    builder.add_node("targeted_gap_research", nodes.targeted_gap_research, retry_policy=retry)
    builder.add_node("generate_report", nodes.generate_report, retry_policy=retry)
    builder.add_node("generate_degraded_report", nodes.generate_degraded_report, retry_policy=retry)
    builder.add_node("persist_report", nodes.persist_report, retry_policy=retry)

    builder.add_edge(START, "plan_research")
    builder.add_edge("plan_research", "build_search_queries")
    builder.add_edge("build_search_queries", "fetch_sources")
    builder.add_edge("fetch_sources", "extract_company_facts")
    builder.add_edge("extract_company_facts", "analyze_business_signals")
    builder.add_edge("analyze_business_signals", "quality_check")
    builder.add_conditional_edges(
        "quality_check",
        route_quality,
        {
            "generate_report": "generate_report",
            "targeted_gap_research": "targeted_gap_research",
            "generate_degraded_report": "generate_degraded_report",
        },
    )
    builder.add_edge("targeted_gap_research", "extract_company_facts")
    builder.add_edge("generate_report", "persist_report")
    builder.add_edge("generate_degraded_report", "persist_report")
    builder.add_edge("persist_report", END)
    return builder.compile(checkpointer=checkpointer)

