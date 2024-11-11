from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from src.config import get_config, set_config
from supabase import AClient, acreate_client
from utils.exceptions import ClientInitializationError, get_error_id
from utils.logger import logger

supabase_client: AClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: ARG001
    """
    Asynchronous context manager that manages the lifespan of the FastAPI application.

    During startup, it initializes the global Supabase client and adds a session.
    When the application shuts down, it logs the user out of Supabase.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Yields control during the lifespan of the application.

    """
    logger.info("Client - Adding session")
    global supabase_client  # noqa: PLW0603
    supabase_client = await create_supabase()
    yield
    await supabase_client.auth.sign_out()


async def create_supabase() -> AClient:
    """
    Create and return an asynchronous Supabase client.

    This contains a workaround for passing through the
    environment to the Configuration class.

    Returns:
        AClient: An instance of the asynchronous Supabase client.

    """
    logger.info("Client - Connecting to supabase instance")

    load_dotenv()
    set_config(os.getenv("ENVIRONMENT"))
    config = get_config()

    return await acreate_client(
        config.api_url,
        config.api_key,
    )


def get_supabase_client() -> AClient:
    """
    Retrieve the initialized Supabase client.

    If the client has not been initialized, logs an error and raises a ClientInitializationError.

    Returns:
        AClient: The initialized Supabase client.

    Raises:
        ClientInitializationError: If the Supabase client is not initialized.

    """
    if supabase_client is None:
        error_id = get_error_id()
        msg = f"Error ID: {error_id}; Supabase client has not been initialized"
        logger.error(msg)
        raise ClientInitializationError(
            msg,
        )
    logger.info("Client - Session started")
    return supabase_client
