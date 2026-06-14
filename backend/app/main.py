from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers.health import router as health_router
from app.api.v1.routers.sessions import router as sessions_router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging
from app.db.session import build_session_factory, dispose_engine, init_db
from app.workflow.graph import build_checkpointer, build_research_graph


def build_lifespan(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        configure_logging(settings)
        app.state.settings = settings
        engine, session_factory = build_session_factory(settings.database_url)
        app.state.db_engine = engine
        app.state.db_session_factory = session_factory
        await init_db(engine)
        checkpointer_context, checkpointer = await build_checkpointer(settings)
        app.state.checkpointer_context = checkpointer_context
        app.state.research_graph = build_research_graph(checkpointer)
        try:
            yield
        finally:
            if checkpointer_context is not None:
                await checkpointer_context.__aexit__(None, None, None)
            await dispose_engine(engine)

    return lifespan


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = getattr(app.state, "settings", get_settings())
    configure_logging(settings)
    app.state.settings = settings
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    active_settings = settings or get_settings()
    configure_logging(active_settings)
    app = FastAPI(
        title=active_settings.app_name,
        version="0.1.0",
        lifespan=build_lifespan(active_settings),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=active_settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router, prefix="/api/v1", tags=["health"])
    app.include_router(sessions_router, prefix="/api/v1", tags=["sessions"])
    return app


app = create_app()
