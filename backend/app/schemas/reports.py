from datetime import datetime

from app.schemas.common import ApiModel


class ReportSourceRead(ApiModel):
    title: str
    url: str
    snippet: str


class ReportRead(ApiModel):
    id: str
    summary: str
    sections: dict
    quality_findings: list
    unknowns: list
    sources: list[ReportSourceRead]
    created_at: datetime

