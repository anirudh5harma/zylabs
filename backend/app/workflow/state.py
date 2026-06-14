import operator
from typing import Annotated, TypedDict


class ResearchState(TypedDict, total=False):
    session_id: str
    company_name: str
    website: str
    objective: str
    research_plan: list[str]
    search_queries: list[str]
    sources: Annotated[list[dict], operator.add]
    extracted_facts: dict
    business_signals: list[str]
    risks: list[str]
    unknowns: list[str]
    quality_findings: list[str]
    quality_status: str
    final_report: dict
    progress_events: Annotated[list[dict], operator.add]
    errors: Annotated[list[dict], operator.add]
    remaining_quality_attempts: int


def progress_event(node: str, message: str, event_type: str = "progress", **payload: object) -> dict:
    return {"node": node, "message": message, "event_type": event_type, "payload": payload}

