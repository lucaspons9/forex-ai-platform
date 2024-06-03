import logging
from typing import Optional

COLORS = {
    "HEADER": "\033[95m",
    "INFO": "\033[94m",
    "DEBUG": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[1;91m",
    "ENDC": "\033[0m",
}


def configure_logger(logger_name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = CustomFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


class CustomFormatter(logging.Formatter):
    def __init__(
        self, fmt: str = "%(levelname)s: %(message)s", datefmt=None, style: str = "%"
    ):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno == logging.DEBUG:
            color = COLORS["DEBUG"]
        elif record.levelno == logging.INFO:
            color = COLORS["INFO"]
        elif record.levelno == logging.WARNING:
            color = COLORS["WARNING"]
        elif record.levelno == logging.ERROR:
            color = COLORS["ERROR"]
        elif record.levelno == logging.CRITICAL:
            color = COLORS["CRITICAL"]
        else:
            color = COLORS["ENDC"]

        formatted_record = super().format(record)
        return f"{color}{formatted_record}{COLORS['ENDC']}"
