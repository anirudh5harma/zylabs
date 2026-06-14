from fastapi.testclient import TestClient

from conftest import create_research_session


def test_workflow_generates_required_report_sections(client: TestClient) -> None:
    session_id = create_research_session(client)

    run_response = client.post(f"/api/v1/sessions/{session_id}/workflow/start")

    assert run_response.status_code == 200
    assert run_response.json()["status"] == "completed"

    detail_response = client.get(f"/api/v1/sessions/{session_id}")
    detail = detail_response.json()
    assert detail["status"] == "completed"
    assert detail["report"] is not None
    sections = detail["report"]["sections"]
    assert set(sections) >= {
        "company_overview",
        "products_services",
        "target_customers",
        "business_signals",
        "risks_challenges",
        "suggested_discovery_questions",
        "suggested_outreach_strategy",
        "unknowns",
        "sources",
    }
    assert len(detail["workflow_events"]) >= 7
    assert len(detail["report"]["sources"]) >= 2


def test_workflow_stream_replays_persisted_events(client: TestClient) -> None:
    session_id = create_research_session(client)
    client.post(f"/api/v1/sessions/{session_id}/workflow/start")

    with client.stream("GET", f"/api/v1/sessions/{session_id}/workflow/stream") as response:
        body = "".join(response.iter_text())

    assert response.status_code == 200
    assert "event: workflow" in body
    assert "Report ready for persistence" in body


def test_resume_requires_recoverable_workflow_state(client: TestClient) -> None:
    session_id = create_research_session(client)

    response = client.post(f"/api/v1/sessions/{session_id}/workflow/resume")

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "workflow_not_recoverable"
