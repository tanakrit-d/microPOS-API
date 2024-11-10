from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from supabase import AClient, acreate_client
from utils.exceptions import ClientInitializationError, get_error_id
from utils.logger import logger

if TYPE_CHECKING:
    from fastapi import FastAPI


supabase_client: AClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: ARG001
    """
    Asynchronous context manager that manages the lifespan of the FastAPI application.

    During startup, it initializes the global Supabase client and adds a session.
    When the application shuts down, it logs the user out of Supabase.

    Args:
    ----
        app (FastAPI): The FastAPI application instance.

    Yields:
    ------
        None: Yields control during the lifespan of the application.

    """
    logger.info("Adding session ...")
    global supabase_client  # noqa: PLW0603
    supabase_client = await create_supabase()
    yield
    await supabase_client.auth.sign_out()


async def create_supabase() -> AClient:
    """
    Create and return an asynchronous Supabase client.

    The client is created using API credentials retrieved from environment variables.

    Returns
    -------
        AClient: An instance of the asynchronous Supabase client.

    """
    return await acreate_client(
        os.environ["API_URL"],
        os.environ["KEY"],
    )


def get_supabase_client() -> AClient:
    """
    Retrieve the initialized Supabase client.

    If the client has not been initialized, an error is logged, and a
    ClientInitializationError is raised with the error ID for tracking.

    Returns
    -------
        AClient: The initialized Supabase client.

    Raises
    ------
        ClientInitializationError: If the Supabase client is not initialized.

    """
    if supabase_client is None:
        error_id = get_error_id()
        msg = f"Error ID: {error_id}; Supabase client has not been initialized"
        logger.error(msg)
        raise ClientInitializationError(
            msg,
        )
    return supabase_client
