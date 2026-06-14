from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def test_health_endpoint_returns_service_metadata() -> None:
    app = create_app(Settings(app_name="test-research-copilot"))
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "test-research-copilot",
        "version": "0.1.0",
    }

