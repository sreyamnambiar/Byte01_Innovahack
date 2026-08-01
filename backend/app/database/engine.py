"""
DarkTrust – Zero Trust Security Platform
SQLAlchemy Async Engine

Creates and configures the async SQLAlchemy engine used throughout
the application. The engine is created once at startup and reused.
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.logging import get_logger

log = get_logger(__name__)


def create_engine() -> AsyncEngine:
    """
    Create and return a configured async SQLAlchemy engine.

    Configuration:
    - Uses asyncpg driver for non-blocking PostgreSQL operations.
    - Connection pooling tuned via settings.
    - Echo SQL only in debug mode (never in production).

    Returns:
        AsyncEngine: Configured async database engine.
    """
    log.info(
        "Initializing database engine",
        extra={
            "db_pool_size": settings.DB_POOL_SIZE,
            "db_max_overflow": settings.DB_MAX_OVERFLOW,
            "debug": settings.DEBUG,
        },
    )

    engine = create_async_engine(
        settings.DATABASE_URL,
        # Log SQL statements only when debug mode is active
        echo=settings.DEBUG,
        # Connection pool configuration
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        # Recycle connections every 30 minutes to avoid stale connections
        pool_recycle=1800,
        # Ping connections before using to detect dropped connections
        pool_pre_ping=True,
        # JSON serialization (future: custom types)
        json_serializer=None,
    )

    log.info("Database engine created successfully")
    return engine


# ---------------------------------------------------------------------------
# Module-level engine singleton
# ---------------------------------------------------------------------------
# Created once at import time and reused across all requests.
# This avoids the overhead of creating a new engine per request.
engine: AsyncEngine = create_engine()
