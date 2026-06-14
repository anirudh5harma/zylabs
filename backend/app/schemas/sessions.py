from datetime import datetime

from pydantic import AnyUrl, Field

from app.schemas.chat import ChatMessageRead
from app.schemas.common import ApiModel
from app.schemas.reports import ReportRead
from app.schemas.workflows import WorkflowEventRead, WorkflowStepRead


class SessionCreate(ApiModel):
    company_name: str = Field(min_length=2, max_length=240)
    website: AnyUrl
    objective: str = Field(min_length=8, max_length=2000)


class SessionSummary(ApiModel):
    id: str
    company_name: str
    website: str
    objective: str
    status: str
    created_at: datetime
    updated_at: datetime
    report_available: bool = False


class SessionDetail(SessionSummary):
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    workflow_steps: list[WorkflowStepRead] = Field(default_factory=list)
    workflow_events: list[WorkflowEventRead] = Field(default_factory=list)
    report: ReportRead | None = None
    chat_messages: list[ChatMessageRead] = Field(default_factory=list)

