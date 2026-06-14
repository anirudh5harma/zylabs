from app.integrations.search_client import SearchResult


class PageFetcher:
    async def fetch(self, result: SearchResult) -> dict:
        raise NotImplementedError


class LocalPageFetcher(PageFetcher):
    async def fetch(self, result: SearchResult) -> dict:
        return {
            "title": result.title,
            "url": result.url,
            "content": result.snippet,
            "snippet": result.snippet,
        }

