from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.api.category.router import router as category_routes
from src.api.item.router import router as item_routes
from src.config import get_config, set_config
from src.database import lifespan
from utils.logger import logger


def create_app() -> FastAPI:
    """
    Initialize the FastAPI application.

    This contains a workaround for passing through the
    environment to the FastAPI app as uvicorn spawns a new process.

    Returns:
        Configured FastAPI application instance

    """
    load_dotenv()
    set_config(os.getenv("ENVIRONMENT"))
    config = get_config()

    logger.info(f"FastAPI - Initializing in {config.environment} environment")

    limiter = Limiter(key_func=get_remote_address)

    app = FastAPI(
        title="microPOS API",
        summary="Middleware layer for interfacing between the app and supabase.",
        lifespan=lifespan,
    )

    app.state.env = os.getenv("ENVIRONMENT")
    app.state.limiter = limiter
    app.state.settings = config

    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    logger.info("FastAPI - Adding routes")
    app.include_router(category_routes)
    app.include_router(item_routes)

    return app


app = create_app()
