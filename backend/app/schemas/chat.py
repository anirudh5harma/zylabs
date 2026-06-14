from datetime import datetime

from pydantic import Field

from app.schemas.common import ApiModel


class ChatRequest(ApiModel):
    message: str = Field(min_length=2, max_length=2000)


class ChatMessageRead(ApiModel):
    id: str
    role: str
    content: str
    sources: list
    created_at: datetime


class ChatResponse(ApiModel):
    user_message: ChatMessageRead
    response_message: ChatMessageRead

