# src/app.py
from __future__ import annotations

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.api.category.router import router as category_routes
from src.api.item.router import router as item_routes
from src.config import get_settings
from src.database import lifespan
from utils.logger import logger


def create_app(env: str | None = None) -> FastAPI:
    """
    Initialize the FastAPI application.

    Args:
        env: Optional environment name to load specific configuration

    Returns:
        Configured FastAPI application instance

    """
    logger.info(f"Starting app in {env or 'default'} environment...")

    settings = get_settings(env)

    limiter = Limiter(key_func=get_remote_address)

    app = FastAPI(
        title="microPOS API",
        summary="Middleware layer for interfacing between the app and supabase.",
        version=settings.VERSION,
        lifespan=lifespan,
        debug=settings.DEBUG,
    )

    app.state.limiter = limiter
    app.state.settings = settings

    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    logger.info("Adding routes...")
    app.include_router(category_routes)
    app.include_router(item_routes)

    return app

app = create_app()
