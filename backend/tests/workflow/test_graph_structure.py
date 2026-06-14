from app.workflow.graph import build_research_graph


def test_graph_uses_multiple_meaningful_nodes() -> None:
    graph = build_research_graph()
    mermaid = graph.get_graph().draw_mermaid()

    assert "plan_research" in mermaid
    assert "quality_check" in mermaid
    assert "generate_report" in mermaid
    assert mermaid.count("-->") >= 8

