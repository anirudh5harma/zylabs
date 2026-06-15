from app.core.config import Settings
from app.integrations.model_client import LocalModelClient, ModelClient
from app.integrations.openai_model_client import OpenAIModelClient
from app.integrations.page_fetcher import LocalPageFetcher, PageFetcher
from app.integrations.search_client import LocalSearchClient, SearchClient


class ProviderConfigurationError(RuntimeError):
    pass


def build_model_client(settings: Settings) -> ModelClient:
    provider = settings.model_provider.strip().lower()
    if provider == "local":
        return LocalModelClient()
    if provider == "openai":
        api_key = (settings.openai_api_key or "").strip()
        if not api_key:
            raise ProviderConfigurationError(
                "OPENAI_API_KEY is required when MODEL_PROVIDER=openai."
            )
        return OpenAIModelClient(api_key=api_key, model_name=settings.model_name)
    raise ProviderConfigurationError(f"Unsupported MODEL_PROVIDER: {settings.model_provider}.")


def build_search_client(settings: Settings) -> SearchClient:
    provider = settings.search_provider.strip().lower()
    if provider == "local":
        return LocalSearchClient()
    raise ProviderConfigurationError(f"Unsupported SEARCH_PROVIDER: {settings.search_provider}.")


def build_page_fetcher() -> PageFetcher:
    return LocalPageFetcher()
