from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.api.category.router import router as category_routes
from src.api.item.router import router as item_routes
from src.database import lifespan
from utils.logging import logger

load_dotenv()


def create_app() -> FastAPI:
    """Initialise the FastAPI application."""
    logger.info("Starting app ...")
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI(
        title="microPOS API",
        summary="Middleware layer for interfacing between the app and supabase.",
        version=os.environ["VERSION"],
        lifespan=lifespan,
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("Adding routes ...")
    app.include_router(category_routes)
    app.include_router(item_routes)
    return app


app = create_app()
