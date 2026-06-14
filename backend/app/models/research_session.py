from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.common import new_id, utc_now


class ResearchSession(Base):
    __tablename__ = "research_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    company_name: Mapped[str] = mapped_column(String(240), nullable=False)
    website: Mapped[str] = mapped_column(String(500), nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="created", index=True)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    events = relationship("WorkflowEvent", cascade="all, delete-orphan")
    steps = relationship("WorkflowStep", cascade="all, delete-orphan")
    report = relationship("ResearchReport", cascade="all, delete-orphan", uselist=False)
    chat_messages = relationship("ChatMessage", cascade="all, delete-orphan")

