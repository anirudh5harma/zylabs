from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers.health import router as health_router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging


def build_lifespan(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        configure_logging(settings)
        app.state.settings = settings
        yield

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
    return app


app = create_app()
