from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.common import new_id, utc_now


class ResearchReport(Base):
    __tablename__ = "research_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    session_id: Mapped[str] = mapped_column(
        ForeignKey("research_sessions.id", ondelete="CASCADE"), unique=True, index=True
    )
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    sections: Mapped[dict] = mapped_column(JSON, nullable=False)
    quality_findings: Mapped[list] = mapped_column(JSON, default=list)
    unknowns: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    sources = relationship("ReportSource", cascade="all, delete-orphan")

