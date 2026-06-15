import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import InvalidStateError
from app.repositories.reports import ReportRepository
from app.repositories.sessions import SessionRepository
from app.repositories.workflow_events import WorkflowEventRepository
from app.schemas.workflows import WorkflowEventRead, WorkflowRunResponse


class WorkflowRunner:
    def __init__(self, db: AsyncSession, graph) -> None:
        self.db = db
        self.graph = graph
        self.sessions = SessionRepository(db)
        self.events = WorkflowEventRepository(db)
        self.reports = ReportRepository(db)

    async def run(self, session_id: str) -> WorkflowRunResponse:
        session = await self.sessions.get(session_id)
        if session.status == "running":
            raise InvalidStateError("workflow_running", "Workflow is already running.")
        return await self._execute(session_id, session.id, reset_steps=True)

    async def resume(self, session_id: str) -> WorkflowRunResponse:
        session = await self.sessions.get(session_id)
        if session.status not in {"running", "failed", "needs_attention"}:
            raise InvalidStateError(
                "workflow_not_recoverable", "Only running or failed workflows can be resumed."
            )
        await self.events.append(
            session_id,
            "resume",
            "Workflow resume requested.",
            "recovery",
            {"status": session.status},
        )
        return await self._execute(session_id, session.id, reset_steps=session.status != "running")

    async def _execute(
        self, session_id: str, checkpoint_thread_id: str, reset_steps: bool
    ) -> WorkflowRunResponse:
        session = await self.sessions.get(session_id)
        if reset_steps:
            await self.events.reset_steps(session_id)
        await self.sessions.set_status(session, "running")
        input_state = {
            "session_id": session.id,
            "company_name": session.company_name,
            "website": session.website,
            "objective": session.objective,
            "sources": [],
            "progress_events": [],
            "errors": [],
            "remaining_quality_attempts": 1,
        }
        config = {"configurable": {"thread_id": checkpoint_thread_id}}
        try:
            final_state = await self.graph.ainvoke(input_state, config=config, durability="sync")
        except Exception as exc:
            await self.events.append(
                session_id,
                "workflow",
                "Workflow failed.",
                "error",
                {"error": str(exc)},
            )
            session = await self.sessions.get(session_id)
            await self.sessions.set_status(session, "failed", str(exc))
            raise
        await self._persist_progress_events(session_id, final_state.get("progress_events", []))
        final_report = final_state["final_report"]
        sources = final_report["sections"]["sources"]
        await self.reports.upsert(
            session_id=session_id,
            summary=final_report["summary"],
            sections=final_report["sections"],
            sources=sources,
            quality_findings=final_state.get("quality_findings", []),
            unknowns=final_state.get("unknowns", []),
        )
        session = await self.sessions.get(session_id)
        await self.sessions.set_status(session, "completed")
        events = await self.events.list(session_id)
        return WorkflowRunResponse(
            session_id=session_id,
            status="completed",
            events=[WorkflowEventRead.model_validate(event) for event in events],
        )

    async def _persist_progress_events(self, session_id: str, events: list[dict]) -> None:
        for event in events:
            node = event["node"]
            message = event["message"]
            event_type = event.get("event_type", "progress")
            payload = event.get("payload", {})
            await self.events.mark_step(session_id, node, "completed", message)
            await self.events.append(session_id, node, message, event_type, payload)

    async def stream_events(self, session_id: str):
        await self.sessions.get(session_id)
        events = await self.events.list(session_id)
        for event in events:
            data = WorkflowEventRead.model_validate(event).model_dump_json()
            yield f"event: workflow\ndata: {data}\n\n"
        yield f"event: done\ndata: {json.dumps({'session_id': session_id})}\n\n"
