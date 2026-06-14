from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str


class SearchClient:
    async def search(self, query: str) -> list[SearchResult]:
        raise NotImplementedError


class LocalSearchClient(SearchClient):
    async def search(self, query: str) -> list[SearchResult]:
        company = query.split(" ")[0].strip() or "Company"
        return [
            SearchResult(
                title=f"{company} company profile",
                url=f"https://example.com/{company.lower()}/profile",
                snippet=f"{company} sells workflow software to revenue and operations teams.",
            ),
            SearchResult(
                title=f"{company} market signals",
                url=f"https://example.com/{company.lower()}/signals",
                snippet=f"{company} is hiring in sales, expanding partnerships, and investing in customer success.",
            ),
        ]

