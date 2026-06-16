from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workflow_event import WorkflowEvent
from app.models.workflow_step import WorkflowStep


WORKFLOW_STEPS = [
    ("plan_research", "Plan research"),
    ("build_search_queries", "Build search queries"),
    ("fetch_sources", "Fetch sources"),
    ("extract_company_facts", "Extract company facts"),
    ("analyze_business_signals", "Analyze business signals"),
    ("quality_check", "Quality check"),
    ("targeted_gap_research", "Targeted gap research"),
    ("generate_report", "Generate report"),
    ("generate_degraded_report", "Generate degraded report"),
    ("persist_report", "Persist report"),
]


class WorkflowEventRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def reset_steps(self, session_id: str) -> None:
        await self.db.execute(delete(WorkflowStep).where(WorkflowStep.session_id == session_id))
        for index, (name, label) in enumerate(WORKFLOW_STEPS, start=1):
            self.db.add(
                WorkflowStep(
                    session_id=session_id,
                    name=name,
                    label=label,
                    sequence=index,
                    status="pending",
                )
            )
        await self.db.commit()

    async def mark_step(self, session_id: str, node: str, status: str, detail: str | None) -> None:
        step = await self.db.scalar(
            select(WorkflowStep).where(WorkflowStep.session_id == session_id, WorkflowStep.name == node)
        )
        if step is None:
            return
        now = datetime.now(timezone.utc)
        step.status = status
        step.detail = detail
        if status == "running" and step.started_at is None:
            step.started_at = now
        if status in {"completed", "failed"}:
            step.completed_at = now
        await self.db.commit()

    async def append(
        self,
        session_id: str,
        node: str,
        message: str,
        event_type: str = "progress",
        payload: dict | None = None,
    ) -> WorkflowEvent:
        event = WorkflowEvent(
            session_id=session_id,
            node=node,
            event_type=event_type,
            message=message,
            payload=payload or {},
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def list(self, session_id: str, after_id: int | None = None) -> list[WorkflowEvent]:
        statement = (
            select(WorkflowEvent)
            .where(WorkflowEvent.session_id == session_id)
            .order_by(WorkflowEvent.id.asc())
        )
        if after_id is not None:
            statement = statement.where(WorkflowEvent.id > after_id)
        result = await self.db.scalars(statement)
        return list(result.all())

    async def list_steps(self, session_id: str) -> list[WorkflowStep]:
        result = await self.db.scalars(
            select(WorkflowStep)
            .where(WorkflowStep.session_id == session_id)
            .order_by(WorkflowStep.sequence.asc())
        )
        return list(result.all())
