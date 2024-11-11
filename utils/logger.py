import logging
from datetime import UTC, datetime
from pathlib import Path


class LoggerSetup:  # noqa: D101
    _logger: logging.Logger | None = None

    @classmethod
    def get_logger(cls, name: str = "micropos-api") -> logging.Logger:
        """Get or create a singleton logger instance."""
        if cls._logger is None:
            cls._logger = cls._init_logging(name)
        return cls._logger

    @staticmethod
    def _init_logging(name: str) -> logging.Logger:
        """Create logger with logs stored in a timestamped folder."""
        logs_dir = Path("logs")
        if not logs_dir.exists():
            logs_dir.mkdir()

        timestamped_folder = datetime.now(UTC).strftime("%Y-%m-%d")
        log_folder_path = logs_dir / timestamped_folder

        if not log_folder_path.exists():
            log_folder_path.mkdir(parents=True)

        log_file = log_folder_path / "micropos-api.log"

        logger = logging.getLogger(name)

        if not logger.handlers:
            file_handler = logging.FileHandler(str(log_file))
            file_handler.setLevel(logging.INFO)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            logger.setLevel(logging.INFO)

        return logger


logger = LoggerSetup.get_logger()
