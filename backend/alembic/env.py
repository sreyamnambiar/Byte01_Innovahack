"""
DarkTrust – Zero Trust Security Platform
Alembic Migration Environment

Configures Alembic to work with SQLAlchemy's async engine using a
synchronous bridge, which is the recommended pattern for async SQLAlchemy
with Alembic.

The database URL is loaded from environment variables (not hardcoded),
following security best practices.
"""

import asyncio
from logging.config import fileConfig
from typing import Optional

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ---------------------------------------------------------------------------
# Import application components
# ---------------------------------------------------------------------------
# Add the backend directory to the Python path so imports resolve correctly
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import settings
from app.database.base import Base

# ---------------------------------------------------------------------------
# Alembic Config object
# ---------------------------------------------------------------------------
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# Model metadata for autogenerate support
# ---------------------------------------------------------------------------
# Import all models here so their tables are registered in metadata.
# As models are added in future modules, import them below:
#
# from app.models.user import User
# from app.models.policy import Policy
# from app.models.audit_log import AuditLog

target_metadata = Base.metadata

# ---------------------------------------------------------------------------
# Set the database URL from application settings
# ---------------------------------------------------------------------------
# Use the sync URL since Alembic uses synchronous connections internally.
config.set_main_option("sqlalchemy.url", settings.DATABASE_SYNC_URL)


# ---------------------------------------------------------------------------
# Offline migrations (generate SQL without connecting to DB)
# ---------------------------------------------------------------------------
def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Configures the context with just a URL, without creating an Engine.
    Generates migration SQL scripts that can be reviewed and executed manually.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,              # Detect column type changes
        compare_server_default=True,    # Detect server default changes
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online migrations (run directly against the database)
# ---------------------------------------------------------------------------
def do_run_migrations(connection: Connection) -> None:
    """Execute migrations using the provided synchronous connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Run migrations using an async engine with a sync bridge.

    Alembic requires synchronous connections internally, so we use
    `run_sync` to bridge the async engine with synchronous migration logic.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # No connection pooling during migrations
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using asyncio."""
    asyncio.run(run_async_migrations())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
