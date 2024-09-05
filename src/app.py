from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.item.router import router
from src.database import lifespan
from utils.logging import logger

load_dotenv()


def create_app() -> FastAPI:
    """Initialise the FastAPI application."""
    logger.info("Starting app ...")
    app = FastAPI(
        title="microPOS API",
        summary="Middleware layer for interfacing between the app and supabase.",
        version=os.environ["VERSION"],
        lifespan=lifespan,
    )
    logger.info("Adding routes ...")
    app.include_router(router)
    return app


app = create_app()
