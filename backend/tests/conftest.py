from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    settings = Settings(
        app_env="test",
        app_name="test-research-copilot",
        database_url=f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        langgraph_checkpoint_url=None,
        backend_cors_origins=["http://testserver"],
    )
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client


def create_research_session(client: TestClient) -> str:
    response = client.post(
        "/api/v1/sessions",
        json={
            "company_name": "Zeno Systems",
            "website": "https://zeno.example",
            "objective": "Prepare for an enterprise sales meeting",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]
