import argparse
import asyncio

from src.config import Environment, set_config
from utils.logger import logger
from utils.seeder import main

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

    set_config(args.env)

    logger.info("Seeder - Starting seeding process ...")

    asyncio.run(main(items=args.count))
