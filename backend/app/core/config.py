from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    app_name: str = "research-copilot"
    log_level: str = "INFO"
    database_url: str = "sqlite+aiosqlite:///./research_copilot.db"
    langgraph_checkpoint_url: str | None = None
    backend_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    model_provider: str = "local"
    model_name: str = "local-research-model"
    openai_api_key: str | None = None
    search_provider: str = "local"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

