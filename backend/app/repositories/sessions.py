from datetime import datetime, timezone

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.errors import NotFoundError
from app.models.research_session import ResearchSession


class SessionRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, company_name: str, website: str, objective: str) -> ResearchSession:
        session = ResearchSession(company_name=company_name, website=website, objective=objective)
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def list(self) -> list[ResearchSession]:
        result = await self.db.scalars(
            select(ResearchSession).order_by(ResearchSession.created_at.desc())
        )
        return list(result.all())

    async def get(self, session_id: str, include_children: bool = False) -> ResearchSession:
        statement: Select[tuple[ResearchSession]] = select(ResearchSession).where(
            ResearchSession.id == session_id
        )
        if include_children:
            statement = statement.options(
                selectinload(ResearchSession.steps),
                selectinload(ResearchSession.events),
                selectinload(ResearchSession.report),
                selectinload(ResearchSession.chat_messages),
            )
        result = await self.db.scalar(statement)
        if result is None:
            raise NotFoundError("session_not_found", "Research session was not found.")
        return result

    async def set_status(
        self, session: ResearchSession, status: str, error_message: str | None = None
    ) -> ResearchSession:
        now = datetime.now(timezone.utc)
        session.status = status
        session.error_message = error_message
        session.updated_at = now
        if status == "running" and session.started_at is None:
            session.started_at = now
        if status in {"completed", "failed", "needs_attention"}:
            session.completed_at = now
        await self.db.commit()
        await self.db.refresh(session)
        return session

