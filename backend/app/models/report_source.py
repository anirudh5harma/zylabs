from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReportSource(Base):
    __tablename__ = "report_sources"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    report_id: Mapped[str] = mapped_column(
        ForeignKey("research_reports.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    url: Mapped[str] = mapped_column(String(700), nullable=False)
    snippet: Mapped[str] = mapped_column(Text, nullable=False)

