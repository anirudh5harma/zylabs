from app.integrations.model_client import ModelClient
from app.integrations.page_fetcher import PageFetcher
from app.integrations.search_client import SearchClient
from app.workflow.state import ResearchState, progress_event


class ResearchNodes:
    def __init__(
        self, search_client: SearchClient, page_fetcher: PageFetcher, model_client: ModelClient
    ) -> None:
        self.search_client = search_client
        self.page_fetcher = page_fetcher
        self.model_client = model_client

    async def plan_research(self, state: ResearchState) -> dict:
        plan = [
            "Understand company positioning",
            "Gather product and customer evidence",
            "Identify business signals and risks",
            "Prepare outreach and discovery guidance",
        ]
        return {
            "research_plan": plan,
            "remaining_quality_attempts": state.get("remaining_quality_attempts", 1),
            "progress_events": [
                progress_event("plan_research", "Research plan created.", plan=plan)
            ],
        }

    async def build_search_queries(self, state: ResearchState) -> dict:
        company = state["company_name"]
        objective = state["objective"]
        queries = [
            f"{company} company overview products customers",
            f"{company} business signals risks hiring partnerships",
            f"{company} {objective}",
        ]
        return {
            "search_queries": queries,
            "progress_events": [
                progress_event("build_search_queries", "Search queries prepared.", count=len(queries))
            ],
        }

    async def fetch_sources(self, state: ResearchState) -> dict:
        collected: list[dict] = []
        for query in state.get("search_queries", []):
            results = await self.search_client.search(query)
            for result in results:
                page = await self.page_fetcher.fetch(result)
                collected.append(page)
        deduped = list({source["url"]: source for source in collected}.values())
        return {
            "sources": deduped,
            "progress_events": [
                progress_event("fetch_sources", "Sources collected.", count=len(deduped))
            ],
        }

    async def extract_company_facts(self, state: ResearchState) -> dict:
        sources = state.get("sources", [])
        facts = {
            "positioning": [source["snippet"] for source in sources[:2]],
            "source_count": len(sources),
        }
        return {
            "extracted_facts": facts,
            "progress_events": [
                progress_event(
                    "extract_company_facts",
                    "Company facts extracted.",
                    source_count=len(sources),
                )
            ],
        }

    async def analyze_business_signals(self, state: ResearchState) -> dict:
        company = state["company_name"]
        signals = [
            f"{company} shows signs of go-to-market investment.",
            "Hiring and partnership language suggest growth priorities.",
            "Customer-facing operations appear central to the business.",
        ]
        risks = [
            "Public information may lag behind current priorities.",
            "Competitive positioning needs validation with the buyer.",
        ]
        unknowns = [
            "Current budget owner",
            "Existing research and enablement tools",
            "Urgency of the upcoming initiative",
        ]
        return {
            "business_signals": signals,
            "risks": risks,
            "unknowns": unknowns,
            "progress_events": [
                progress_event("analyze_business_signals", "Business signals analyzed.")
            ],
        }

    async def quality_check(self, state: ResearchState) -> dict:
        findings: list[str] = []
        if len(state.get("sources", [])) < 2:
            findings.append("Report needs at least two sources.")
        if not state.get("business_signals"):
            findings.append("Business signals are missing.")
        status = "pass"
        if findings and state.get("remaining_quality_attempts", 0) > 0:
            status = "gaps"
        elif findings:
            status = "unrecoverable"
        return {
            "quality_findings": findings,
            "quality_status": status,
            "progress_events": [
                progress_event("quality_check", f"Quality check result: {status}.", findings=findings)
            ],
        }

    async def targeted_gap_research(self, state: ResearchState) -> dict:
        company = state["company_name"]
        result = await self.search_client.search(f"{company} customer proof and risks")
        fetched = [await self.page_fetcher.fetch(item) for item in result]
        remaining = max(state.get("remaining_quality_attempts", 1) - 1, 0)
        return {
            "sources": fetched,
            "remaining_quality_attempts": remaining,
            "progress_events": [
                progress_event("targeted_gap_research", "Targeted gap research completed.")
            ],
        }

    async def generate_report(self, state: ResearchState) -> dict:
        report = await self.model_client.generate_report(dict(state), degraded=False)
        return {
            "final_report": report,
            "progress_events": [
                progress_event("generate_report", "Structured report generated.")
            ],
        }

    async def generate_degraded_report(self, state: ResearchState) -> dict:
        report = await self.model_client.generate_report(dict(state), degraded=True)
        return {
            "final_report": report,
            "progress_events": [
                progress_event(
                    "generate_degraded_report",
                    "Degraded report generated with unknowns preserved.",
                    event_type="warning",
                )
            ],
        }

    async def record_node_error(self, state: ResearchState) -> dict:
        return {
            "errors": [{"node": "workflow", "message": "Recoverable workflow issue recorded."}],
            "quality_status": "unrecoverable",
            "progress_events": [
                progress_event(
                    "record_node_error",
                    "Workflow issue recorded for degraded output.",
                    event_type="warning",
                )
            ],
        }

    async def persist_report(self, state: ResearchState) -> dict:
        return {
            "progress_events": [
                progress_event("persist_report", "Report ready for persistence.")
            ],
        }

