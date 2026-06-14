from fastapi.testclient import TestClient

from conftest import create_research_session


def test_chat_requires_completed_report(client: TestClient) -> None:
    session_id = create_research_session(client)

    response = client.post(
        f"/api/v1/sessions/{session_id}/chat",
        json={"message": "What should I ask first?"},
    )

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "report_not_ready"


def test_chat_uses_completed_report_context(client: TestClient) -> None:
    session_id = create_research_session(client)
    client.post(f"/api/v1/sessions/{session_id}/workflow/start")

    response = client.post(
        f"/api/v1/sessions/{session_id}/chat",
        json={"message": "What should I ask first?"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["user_message"]["role"] == "user"
    assert payload["response_message"]["role"] == "response"
    assert "saved briefing" in payload["response_message"]["content"]
    assert payload["response_message"]["sources"]

    history_response = client.get(f"/api/v1/sessions/{session_id}/chat")
    assert len(history_response.json()) == 2
