import argparse

from src.config import Environment, set_config
from utils.logger import logger

"""
This file is validating the initialization of the Configuration class.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of items to seed",
    )
    parser.add_argument(
        "--env",
        type=str,
        choices=[e.value for e in Environment],
        default=None,
        help="Environment to seed (local, development, staging, production)",
    )
    args = parser.parse_args()

    if args.env:
        try:
            set_config(args.env)
        except ValueError as ve:
            logger.error(f"Invalid environment value provided: {ve}")
        except FileNotFoundError as fnf_error:
            logger.error(f"Configuration file not found: {fnf_error}")
        except ImportError as import_error:
            logger.error(f"Failed to import configuration module: {import_error}")

