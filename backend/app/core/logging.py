"""
DarkTrust – Zero Trust Security Platform
Structured Logging Configuration

Configures Loguru for structured, production-grade logging.
Supports both human-readable (text) and machine-parseable (JSON) formats.
"""

import logging
import sys
from typing import Any

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Intercept standard library logging calls and redirect them to Loguru.

    This ensures that third-party libraries (SQLAlchemy, Uvicorn, etc.)
    that use the standard `logging` module are captured by Loguru's
    centralized logging system.
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Find the corresponding Loguru level
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find the caller that originated the log message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore[assignment]
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(log_level: str = "INFO", log_format: str = "json") -> None:
    """
    Initialize the application logging system.

    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format: Output format — "json" for structured logs, "text" for human-readable.

    Should be called once at application startup, before any other initialization.
    """
    # Remove all existing Loguru handlers
    logger.remove()

    if log_format.lower() == "json":
        # Structured JSON format — ideal for log aggregators (Datadog, ELK, etc.)
        fmt = (
            '{{"time":"{time:YYYY-MM-DDTHH:mm:ss.SSS}Z",'
            '"level":"{level}",'
            '"name":"{name}",'
            '"function":"{function}",'
            '"line":{line},'
            '"message":"{message}"}}'
        )
    else:
        # Human-readable format — ideal for local development
        fmt = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    logger.add(
        sys.stdout,
        format=fmt,
        level=log_level.upper(),
        colorize=(log_format.lower() != "json"),
        backtrace=True,
        diagnose=True,
        enqueue=True,  # Thread-safe async logging
    )

    # Intercept standard library loggers
    _intercept_standard_loggers()

    logger.info(
        "Logging initialized",
        extra={"level": log_level, "format": log_format},
    )


def _intercept_standard_loggers() -> None:
    """
    Replace handlers for common third-party loggers with InterceptHandler.

    Ensures uniform log formatting across the entire application stack.
    """
    third_party_loggers = [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "sqlalchemy.engine",
        "sqlalchemy.pool",
        "alembic",
    ]

    handler = InterceptHandler()

    for logger_name in third_party_loggers:
        lib_logger = logging.getLogger(logger_name)
        lib_logger.handlers = [handler]
        lib_logger.propagate = False

    # Root logger intercept
    logging.basicConfig(handlers=[handler], level=0, force=True)


def get_logger(name: str) -> Any:
    """
    Return a named Loguru logger instance.

    Args:
        name: Module name (use __name__ for automatic naming).

    Returns:
        A bound Loguru logger with the given name context.

    Usage:
        log = get_logger(__name__)
        log.info("Processing request", request_id="abc-123")
    """
    return logger.bind(logger_name=name)
