class ModelClient:
    async def generate_report(self, state: dict, degraded: bool = False) -> dict:
        raise NotImplementedError

    async def answer_follow_up(self, report: dict, question: str) -> str:
        raise NotImplementedError


class LocalModelClient(ModelClient):
    async def generate_report(self, state: dict, degraded: bool = False) -> dict:
        company = state["company_name"]
        sources = state.get("sources", [])
        suffix = " Some claims need follow-up validation." if degraded else ""
        return {
            "summary": f"{company} appears to be a B2B company with signals relevant to the stated objective.{suffix}",
            "sections": {
                "company_overview": f"{company} is positioned around operational workflow improvement.",
                "products_services": "Workflow software, research support, enablement tooling, and advisory services.",
                "target_customers": "Revenue leaders, operations teams, account executives, and customer-facing teams.",
                "business_signals": state.get("business_signals", []),
                "risks_challenges": state.get("risks", []),
                "suggested_discovery_questions": [
                    "Which current research workflows slow the team down most?",
                    "How is meeting preparation measured today?",
                    "What sources are trusted when preparing for strategic accounts?",
                ],
                "suggested_outreach_strategy": "Lead with a concise operational pain hypothesis, cite recent signals, and ask for validation instead of pitching immediately.",
                "unknowns": state.get("unknowns", []),
                "sources": sources,
            },
        }

    async def answer_follow_up(self, report: dict, question: str) -> str:
        overview = report["sections"].get("company_overview", "The report has no overview.")
        return (
            f"Based on the saved briefing, {overview} For your question: {question} "
            "The strongest next step is to validate the highest-impact unknowns during discovery."
        )

