from app.models.research_session import ResearchSession
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.reports import ReportRepository
from app.repositories.sessions import SessionRepository
from app.repositories.workflow_events import WorkflowEventRepository
from app.schemas.chat import ChatMessageRead
from app.schemas.reports import ReportRead
from app.schemas.sessions import SessionDetail, SessionSummary
from app.schemas.workflows import WorkflowEventRead, WorkflowStepRead


class SessionService:
    def __init__(
        self,
        sessions: SessionRepository,
        workflow_events: WorkflowEventRepository,
        reports: ReportRepository,
        chat_messages: ChatMessageRepository,
    ) -> None:
        self.sessions = sessions
        self.workflow_events = workflow_events
        self.reports = reports
        self.chat_messages = chat_messages

    async def create(self, company_name: str, website: str, objective: str) -> SessionSummary:
        session = await self.sessions.create(company_name, website, objective)
        return self._summary(session, report_available=False)

    async def list(self) -> list[SessionSummary]:
        sessions = await self.sessions.list()
        summaries: list[SessionSummary] = []
        for session in sessions:
            report = await self.reports.get_for_session(session.id)
            summaries.append(self._summary(session, report_available=report is not None))
        return summaries

    async def detail(self, session_id: str) -> SessionDetail:
        session = await self.sessions.get(session_id)
        report = await self.reports.get_for_session(session_id)
        events = await self.workflow_events.list(session_id)
        steps = await self.workflow_events.list_steps(session_id)
        messages = await self.chat_messages.list(session_id)
        summary = self._summary(session, report_available=report is not None)
        return SessionDetail(
            **summary.model_dump(),
            error_message=session.error_message,
            started_at=session.started_at,
            completed_at=session.completed_at,
            workflow_steps=[WorkflowStepRead.model_validate(step) for step in steps],
            workflow_events=[WorkflowEventRead.model_validate(event) for event in events],
            report=ReportRead.model_validate(report) if report else None,
            chat_messages=[ChatMessageRead.model_validate(message) for message in messages],
        )

    def _summary(self, session: ResearchSession, report_available: bool) -> SessionSummary:
        return SessionSummary(
            id=session.id,
            company_name=session.company_name,
            website=session.website,
            objective=session.objective,
            status=session.status,
            created_at=session.created_at,
            updated_at=session.updated_at,
            report_available=report_available,
        )

