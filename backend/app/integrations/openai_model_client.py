import json
from typing import Any

import httpx

from app.integrations.model_client import ModelClient, ModelProviderError


class OpenAIModelClient(ModelClient):
    api_url = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key: str, model_name: str, timeout_seconds: float = 45.0) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.timeout_seconds = timeout_seconds

    async def generate_report(self, state: dict, degraded: bool = False) -> dict:
        sources = [self._source_payload(source) for source in state.get("sources", [])]
        prompt = {
            "company_name": state["company_name"],
            "website": state["website"],
            "objective": state["objective"],
            "research_plan": state.get("research_plan", []),
            "sources": sources,
            "business_signals": state.get("business_signals", []),
            "risks": state.get("risks", []),
            "unknowns": state.get("unknowns", []),
            "degraded": degraded,
        }
        content = await self._chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create concise sales research briefings. Use only the provided "
                        "source material. Preserve uncertainty in the unknowns section."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Create a structured briefing as JSON for this research state:\n"
                        f"{json.dumps(prompt, ensure_ascii=True)}"
                    ),
                },
            ],
            response_format=self._report_response_format(),
        )
        try:
            report = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ModelProviderError("OpenAI returned invalid report JSON.") from exc
        return self._normalize_report(report, sources)

    async def answer_follow_up(self, report: dict, question: str) -> str:
        content = await self._chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer follow-up questions using only the saved report context. "
                        "Be concise and cite uncertainty when the report does not answer directly."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {"report": report, "question": question}, ensure_ascii=True
                    ),
                },
            ],
        )
        return content.strip()

    async def _chat_completion(
        self, messages: list[dict[str, str]], response_format: dict[str, Any] | None = None
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.2,
        }
        if response_format is not None:
            payload["response_format"] = response_format
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
        if response.status_code >= 400:
            raise ModelProviderError(self._error_message(response))
        data = response.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ModelProviderError("OpenAI returned an unexpected response shape.") from exc
        if not content:
            raise ModelProviderError("OpenAI returned an empty response.")
        return content

    def _error_message(self, response: httpx.Response) -> str:
        try:
            detail = response.json().get("error", {}).get("message")
        except ValueError:
            detail = None
        if detail:
            return f"OpenAI request failed: {detail}"
        return f"OpenAI request failed with status {response.status_code}."

    def _normalize_report(self, report: dict, sources: list[dict]) -> dict:
        sections = report.get("sections") if isinstance(report.get("sections"), dict) else {}
        defaults: dict[str, Any] = {
            "company_overview": "Not enough verified context was available.",
            "products_services": "Not enough verified context was available.",
            "target_customers": "Not enough verified context was available.",
            "business_signals": [],
            "risks_challenges": [],
            "suggested_discovery_questions": [],
            "suggested_outreach_strategy": "Validate the unknowns before pitching.",
            "unknowns": [],
            "sources": sources,
        }
        normalized_sections = {key: sections.get(key, value) for key, value in defaults.items()}
        normalized_sections["sources"] = sources
        return {
            "summary": str(report.get("summary") or "Research briefing generated."),
            "sections": normalized_sections,
        }

    @staticmethod
    def _source_payload(source: dict) -> dict:
        return {
            "title": str(source.get("title", "")),
            "url": str(source.get("url", "")),
            "snippet": str(source.get("snippet", "")),
        }

    def _report_response_format(self) -> dict[str, Any]:
        source_schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "title": {"type": "string"},
                "url": {"type": "string"},
                "snippet": {"type": "string"},
            },
            "required": ["title", "url", "snippet"],
        }
        sections_schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "company_overview": {"type": "string"},
                "products_services": {"type": "string"},
                "target_customers": {"type": "string"},
                "business_signals": {"type": "array", "items": {"type": "string"}},
                "risks_challenges": {"type": "array", "items": {"type": "string"}},
                "suggested_discovery_questions": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "suggested_outreach_strategy": {"type": "string"},
                "unknowns": {"type": "array", "items": {"type": "string"}},
                "sources": {"type": "array", "items": source_schema},
            },
            "required": [
                "company_overview",
                "products_services",
                "target_customers",
                "business_signals",
                "risks_challenges",
                "suggested_discovery_questions",
                "suggested_outreach_strategy",
                "unknowns",
                "sources",
            ],
        }
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "research_report",
                "strict": True,
                "schema": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "summary": {"type": "string"},
                        "sections": sections_schema,
                    },
                    "required": ["summary", "sections"],
                },
            },
        }
