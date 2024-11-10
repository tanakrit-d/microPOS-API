# src/core/config.py
from __future__ import annotations

import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Environment enumeration for the application."""

    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Settings
    VERSION: str
    API_URL: str
    KEY: str

    # Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False

    # Add any other configuration settings here

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
    )

    @classmethod
    def load_config(cls, env: str | None = None) -> Settings:
        """
        Load configuration based on the specified environment.

        Args:
            env: The environment to load. If None, defaults to ENVIRONMENT
                environment variable or 'development'

        Returns:
            Settings instance with loaded configuration

        """
        # Determine environment
        if env is None:
            env = os.getenv("ENVIRONMENT", "development")

        # Get project root directory
        root_dir = Path(__file__).parent.parent

        # Define possible env files in order of precedence
        env_files = [
            root_dir / f".env.{env}",
            root_dir / ".env.local" if env == "local" else None,
            root_dir / ".env",
        ]

        # Load the first existing env file
        env_file_loaded = None
        for env_file in env_files:
            if env_file and env_file.exists():
                load_dotenv(env_file)
                env_file_loaded = env_file
                break

        if env_file_loaded is None:
            raise FileNotFoundError(
                "No environment file found. Looked for: " +
                ", ".join(str(f) for f in env_files if f),
            )

        return cls()

def get_settings(env: str | None = None) -> Settings:
    """Get application settings singleton."""
    return Settings.load_config(env)
