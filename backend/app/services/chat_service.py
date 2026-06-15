from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import InvalidStateError
from app.integrations.model_client import LocalModelClient, ModelClient
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.reports import ReportRepository
from app.repositories.sessions import SessionRepository
from app.schemas.chat import ChatMessageRead, ChatResponse


class ChatService:
    def __init__(self, db: AsyncSession, model_client: ModelClient | None = None) -> None:
        self.sessions = SessionRepository(db)
        self.reports = ReportRepository(db)
        self.messages = ChatMessageRepository(db)
        self.model_client = model_client or LocalModelClient()

    async def list(self, session_id: str) -> list[ChatMessageRead]:
        await self.sessions.get(session_id)
        messages = await self.messages.list(session_id)
        return [ChatMessageRead.model_validate(message) for message in messages]

    async def ask(self, session_id: str, content: str) -> ChatResponse:
        await self.sessions.get(session_id)
        report = await self.reports.get_for_session(session_id)
        if report is None:
            raise InvalidStateError(
                "report_not_ready", "Follow-up chat is available after the report is generated."
            )
        user_message = await self.messages.append(session_id, "user", content)
        answer = await self.model_client.answer_follow_up(
            {
                "summary": report.summary,
                "sections": report.sections,
                "sources": [
                    {"title": source.title, "url": source.url, "snippet": source.snippet}
                    for source in report.sources
                ],
            },
            content,
        )
        response_message = await self.messages.append(
            session_id,
            "response",
            answer,
            sources=[{"title": source.title, "url": source.url} for source in report.sources[:3]],
        )
        return ChatResponse(
            user_message=ChatMessageRead.model_validate(user_message),
            response_message=ChatMessageRead.model_validate(response_message),
        )
