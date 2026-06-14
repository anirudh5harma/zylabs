from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.errors import AppError, to_http_error
from app.repositories.chat_messages import ChatMessageRepository
from app.repositories.reports import ReportRepository
from app.repositories.sessions import SessionRepository
from app.repositories.workflow_events import WorkflowEventRepository
from app.schemas.chat import ChatMessageRead, ChatRequest, ChatResponse
from app.schemas.sessions import SessionCreate, SessionDetail, SessionSummary
from app.schemas.workflows import WorkflowEventRead, WorkflowRunResponse
from app.services.chat_service import ChatService
from app.services.session_service import SessionService
from app.services.workflow_runner import WorkflowRunner

router = APIRouter()


def build_session_service(db: AsyncSession) -> SessionService:
    return SessionService(
        SessionRepository(db),
        WorkflowEventRepository(db),
        ReportRepository(db),
        ChatMessageRepository(db),
    )


@router.post("/sessions", response_model=SessionSummary, status_code=201)
async def create_session(payload: SessionCreate, db: AsyncSession = Depends(get_db)) -> SessionSummary:
    service = build_session_service(db)
    return await service.create(str(payload.company_name), str(payload.website), payload.objective)


@router.get("/sessions", response_model=list[SessionSummary])
async def list_sessions(db: AsyncSession = Depends(get_db)) -> list[SessionSummary]:
    return await build_session_service(db).list()


@router.get("/sessions/{session_id}", response_model=SessionDetail)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)) -> SessionDetail:
    try:
        return await build_session_service(db).detail(session_id)
    except AppError as error:
        raise to_http_error(error) from error


@router.post("/sessions/{session_id}/workflow/start", response_model=WorkflowRunResponse)
async def start_workflow(
    session_id: str, request: Request, db: AsyncSession = Depends(get_db)
) -> WorkflowRunResponse:
    try:
        runner = WorkflowRunner(db, request.app.state.research_graph)
        return await runner.run(session_id)
    except AppError as error:
        raise to_http_error(error) from error


@router.get("/sessions/{session_id}/workflow/events", response_model=list[WorkflowEventRead])
async def list_workflow_events(
    session_id: str, db: AsyncSession = Depends(get_db)
) -> list[WorkflowEventRead]:
    try:
        await SessionRepository(db).get(session_id)
        events = await WorkflowEventRepository(db).list(session_id)
        return [WorkflowEventRead.model_validate(event) for event in events]
    except AppError as error:
        raise to_http_error(error) from error


@router.get("/sessions/{session_id}/workflow/stream")
async def stream_workflow_events(
    session_id: str, request: Request, db: AsyncSession = Depends(get_db)
) -> StreamingResponse:
    try:
        runner = WorkflowRunner(db, request.app.state.research_graph)
        return StreamingResponse(runner.stream_events(session_id), media_type="text/event-stream")
    except AppError as error:
        raise to_http_error(error) from error


@router.get("/sessions/{session_id}/chat", response_model=list[ChatMessageRead])
async def list_chat(session_id: str, db: AsyncSession = Depends(get_db)) -> list[ChatMessageRead]:
    try:
        return await ChatService(db).list(session_id)
    except AppError as error:
        raise to_http_error(error) from error


@router.post("/sessions/{session_id}/chat", response_model=ChatResponse)
async def ask_chat(
    session_id: str, payload: ChatRequest, db: AsyncSession = Depends(get_db)
) -> ChatResponse:
    try:
        return await ChatService(db).ask(session_id, payload.message)
    except AppError as error:
        raise to_http_error(error) from error
