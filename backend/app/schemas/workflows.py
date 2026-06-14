from datetime import datetime

from app.schemas.common import ApiModel


class WorkflowStepRead(ApiModel):
    name: str
    label: str
    status: str
    sequence: int
    detail: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class WorkflowEventRead(ApiModel):
    id: int
    node: str
    event_type: str
    message: str
    payload: dict
    created_at: datetime


class WorkflowRunResponse(ApiModel):
    session_id: str
    status: str
    events: list[WorkflowEventRead]

