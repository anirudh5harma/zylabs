from typing import Literal

from app.workflow.state import ResearchState


def route_quality(state: ResearchState) -> Literal[
    "generate_report", "targeted_gap_research", "generate_degraded_report"
]:
    status = state.get("quality_status")
    if status == "pass":
        return "generate_report"
    if status == "gaps":
        return "targeted_gap_research"
    return "generate_degraded_report"

