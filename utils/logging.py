import logging
from datetime import datetime, timezone
from pathlib import Path


def init_logging() -> logging.Logger:
    """Create logger with logs stored in a timestamped folder."""
    logs_dir = Path("logs")
    if not logs_dir.exists():
        logs_dir.mkdir()

    timestamped_folder = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_folder_path = logs_dir / timestamped_folder

    if not log_folder_path.exists():
        log_folder_path.mkdir(parents=True)

    log_file = log_folder_path / "output.log"

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=str(log_file),
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    return logger


logger = init_logging()
