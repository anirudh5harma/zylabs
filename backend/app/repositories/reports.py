from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.report_source import ReportSource
from app.models.research_report import ResearchReport


class ReportRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def upsert(
        self,
        session_id: str,
        summary: str,
        sections: dict,
        sources: list[dict],
        quality_findings: list,
        unknowns: list,
    ) -> ResearchReport:
        existing = await self.get_for_session(session_id)
        if existing is not None:
            await self.db.execute(delete(ReportSource).where(ReportSource.report_id == existing.id))
            report = existing
            report.summary = summary
            report.sections = sections
            report.quality_findings = quality_findings
            report.unknowns = unknowns
        else:
            report = ResearchReport(
                session_id=session_id,
                summary=summary,
                sections=sections,
                quality_findings=quality_findings,
                unknowns=unknowns,
            )
            self.db.add(report)
            await self.db.flush()
        for source in sources:
            self.db.add(
                ReportSource(
                    report_id=report.id,
                    title=source["title"],
                    url=source["url"],
                    snippet=source["snippet"],
                )
            )
        await self.db.commit()
        return await self.get_for_session(session_id, required=True)

    async def get_for_session(
        self, session_id: str, required: bool = False
    ) -> ResearchReport | None:
        result = await self.db.scalar(
            select(ResearchReport)
            .where(ResearchReport.session_id == session_id)
            .options(selectinload(ResearchReport.sources))
        )
        if required and result is None:
            raise RuntimeError("Report was expected after upsert.")
        return result

