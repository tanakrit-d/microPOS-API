from __future__ import annotations

from enum import Enum
from pathlib import Path

from dotenv import dotenv_values

from utils.logger import logger


class Environment(str, Enum):
    """Enumeration for different application environments."""

    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Configuration:
    """
    Singleton class for application settings configuration.

    This class loads and holds configuration settings for the application
    based on the defined environment. Settings include the version,
    API URL, API key, environment, and debug flag.
    """

    version: str
    api_url: str
    key: str
    environment: Environment
    debug: bool

    _instance: Configuration | None = None

    @classmethod
    def _to_lower(cls, value: str) -> str:
        """Convert a string to lowercase."""
        return value.lower()

    @classmethod
    def _from_str(cls, value: str | None) -> Environment:
        """
        Convert a string to an Environment Enum.

        This method returns a corresponding Environment member for a
        given string value. If the value is empty or invalid, it defaults
        to DEVELOPMENT.

        Args:
            value (str | None): The environment as a string.

        Returns:
            Environment: The corresponding Environment member.

        Raises:
            ValueError: If the provided value does not match any Environment member.

        """
        if not value:
            return Environment.DEVELOPMENT

        value = cls._to_lower(value)

        if value in Environment.__members__.values():
            return Environment(value)

        msg = f"Config - Invalid environment: '{value}'. Must be one of {[e.value for e in Environment]}"
        logger.error(msg)

        raise ValueError(msg)

    @classmethod
    def _parse_env(cls, env: str | None) -> None:
        """
        Parse the environment and load environment variables from a .env file.

        This method determines the appropriate .env file based on the
        provided environment and loads its variables into the Configuration class.

        Args:
            env (str | None): The environment as a string.

        Raises:
            FileNotFoundError: If the environment file does not exist.

        """
        environment = cls._from_str(env)
        root_dir = Path(__file__).parent.parent
        env_file = root_dir / f".env.{environment.value}"

        if env_file.exists():
            logger.info("Config - Loading from: %s", env_file)
            config = dotenv_values(env_file)
            cls.version = config.get("VERSION")
            cls.api_url = config.get("API_URL")
            cls.api_key = config.get("API_KEY")
            cls.environment = config.get("ENVIRONMENT")
            cls.debug = config.get("DEBUG")
            return

        msg = f"Config - No environment file found for {environment}. Looked for: {env_file}"
        logger.error(msg)

        raise FileNotFoundError(msg)

    @classmethod
    def load_config(cls, env: str | None) -> Configuration:
        """
        Load settings configuration based on the provided environment.

        This method initializes the Configuration instance and loads the
        configuration from the environment variables if not already done.

        Args:
            env (str | None): The environment as a string.

        Returns:
            Configuration: The singleton instance of Configuration containing
            the loaded configuration.

        """
        if cls._instance is None:
            cls._parse_env(env)
            cls._instance = Configuration()
            logger.info("Config - Successfully loaded environment: %s", env)
        return cls._instance

    @classmethod
    def get_instance(cls) -> Configuration:
        """
        Get the current instance of the Configuration class.

        Returns:
            Configuration: The singleton instance of Configuration.

        """
        return cls._instance


def get_config() -> Configuration:
    """
    Retrieve the application settings configuration.

    This function provides access to the singleton instance of Configuration,
    ensuring the configuration is loaded.

    Returns:
        Configuration: The singleton instance of Configuration containing the configuration.

    """
    return Configuration.get_instance()

def set_config(env: str | None) -> None:
    """
    Set the application settings configuration for the specified environment.

    This function acts as a simple interface to load the configuration
    based on the environment string provided. It initializes the settings
    if they are not yet loaded.

    Args:
        env (str | None): The environment as a string.

    """
    Configuration.load_config(env)
