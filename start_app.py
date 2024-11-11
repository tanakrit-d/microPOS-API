import argparse

import uvicorn
from dotenv import set_key

from src.config import Environment

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env",
        type=str,
        choices=[e.value for e in Environment],
        default=None,
        help="Environment to start the app in (local, development, staging, production)",
    )
    args = parser.parse_args()

    """
    Passthrough desired environment by writing it to .env
    This allows us to still load the correct settings when
    uvicorn spawns FastAPI app in a different process.
    """

    set_key(dotenv_path=".env", key_to_set="ENVIRONMENT", value_to_set=args.env)

    uvicorn.run(
        "src.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug",
    )
