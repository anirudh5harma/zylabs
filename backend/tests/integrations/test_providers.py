import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.integrations.model_client import LocalModelClient
from app.integrations.openai_model_client import OpenAIModelClient
from app.integrations.providers import ProviderConfigurationError, build_model_client
from app.main import create_app


def test_local_provider_is_default() -> None:
    client = build_model_client(Settings())

    assert isinstance(client, LocalModelClient)


def test_openai_provider_requires_api_key() -> None:
    settings = Settings(model_provider="openai", openai_api_key="")

    with pytest.raises(ProviderConfigurationError, match="OPENAI_API_KEY is required"):
        build_model_client(settings)


def test_openai_provider_builds_live_client_with_key() -> None:
    settings = Settings(model_provider="openai", openai_api_key="sk-test")

    client = build_model_client(settings)

    assert isinstance(client, OpenAIModelClient)


def test_openai_missing_key_fails_at_startup(tmp_path) -> None:
    settings = Settings(
        app_env="test",
        app_name="test-research-copilot",
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        langgraph_checkpoint_url=None,
        backend_cors_origins=["http://testserver"],
        model_provider="openai",
        openai_api_key="",
    )
    app = create_app(settings)

    with pytest.raises(ProviderConfigurationError, match="OPENAI_API_KEY is required"):
        with TestClient(app):
            pass
