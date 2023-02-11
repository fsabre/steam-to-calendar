"""Define the logger for the project."""

import logging
from typing import Final

# Convenience for me
DEV_MODE: Final[bool] = False
LOG_FORMAT: Final[str] = "%(asctime)s::%(levelname)s::%(message)s"

# Terminal color codes
DARK_GRAY = "\x1b[1;30m"
YELLOW = "\x1b[33;21m"
RED = "\x1b[31;21m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"
FORMATS = {
    logging.DEBUG: DARK_GRAY,
    logging.INFO: "",
    logging.WARNING: YELLOW,
    logging.ERROR: RED,
    logging.CRITICAL: BOLD_RED,
}


class ColoredFormatter(logging.Formatter):
    """Logging formatter with colors depending on the level."""

    def format(self, record: logging.LogRecord) -> str:
        return FORMATS.get(record.levelno, "") + super().format(record) + RESET


logger = logging.getLogger("steam-to-calendar")
logger.setLevel(logging.DEBUG if DEV_MODE else logging.WARNING)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    ColoredFormatter(LOG_FORMAT) if DEV_MODE else logging.Formatter(LOG_FORMAT)
)
logger.addHandler(stream_handler)
