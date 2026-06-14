from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_message import ChatMessage


class ChatMessageRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def append(
        self, session_id: str, role: str, content: str, sources: list | None = None
    ) -> ChatMessage:
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            sources=sources or [],
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def list(self, session_id: str) -> list[ChatMessage]:
        result = await self.db.scalars(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
        )
        return list(result.all())

