from fastapi import APIRouter, Request
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    settings = request.app.state.settings
    return HealthResponse(status="ok", service=settings.app_name, version="0.1.0")

