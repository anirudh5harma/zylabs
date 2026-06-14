from fastapi.testclient import TestClient


def test_create_and_list_sessions(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/sessions",
        json={
            "company_name": "Acme Corp",
            "website": "https://acme.example",
            "objective": "Prepare for a first discovery call",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["company_name"] == "Acme Corp"
    assert created["status"] == "created"

    list_response = client.get("/api/v1/sessions")
    assert list_response.status_code == 200
    assert list_response.json()[0]["id"] == created["id"]


def test_create_session_rejects_invalid_input(client: TestClient) -> None:
    response = client.post(
        "/api/v1/sessions",
        json={"company_name": "A", "website": "not-a-url", "objective": "short"},
    )

    assert response.status_code == 422


def test_get_unknown_session_returns_not_found(client: TestClient) -> None:
    response = client.get("/api/v1/sessions/missing")

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "session_not_found"

