"""
DarkTrust – Zero Trust Security Platform
SQLAlchemy Async Session Factory

Provides the async session factory and FastAPI dependency for
database session injection into route handlers and services.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.engine import engine
from app.core.logging import get_logger

log = get_logger(__name__)

# ---------------------------------------------------------------------------
# Session Factory
# ---------------------------------------------------------------------------
AsyncSessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,   # Prevents lazy-load errors after commit
    autocommit=False,
    autoflush=False,
)
"""
Async session factory bound to the application engine.

expire_on_commit=False is set so that ORM objects remain accessible
after a commit without triggering additional SELECT queries.
"""


# ---------------------------------------------------------------------------
# FastAPI Dependency
# ---------------------------------------------------------------------------
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async database session.

    Opens a session, yields it to the route handler, and ensures
    the session is properly closed after the request completes —
    even if an exception occurs.

    Usage in route handlers:
        @router.get("/example")
        async def example(db: AsyncSession = Depends(get_db_session)):
            result = await db.execute(select(MyModel))
            return result.scalars().all()

    The session uses a context manager to guarantee cleanup.
    Transactions are NOT automatically committed; route handlers
    must explicitly call `await db.commit()` after mutations.
    """
    async with AsyncSessionFactory() as session:
        try:
            log.debug("Database session opened")
            yield session
        except Exception:
            log.exception("Database session error — rolling back")
            await session.rollback()
            raise
        finally:
            await session.close()
            log.debug("Database session closed")
