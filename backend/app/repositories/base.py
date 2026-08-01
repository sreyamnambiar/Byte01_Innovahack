"""
DarkTrust – Zero Trust Security Platform
Generic Async Base Repository

Provides standard CRUD operations for all ORM models using SQLAlchemy 2.0
async style.  Concrete repositories inherit from this class and add
domain-specific query methods.

SOLID adherence:
  - Single Responsibility: only database operations, zero business logic
  - Open/Closed: open for extension via inheritance, closed for modification
  - Liskov: all concrete repos are valid substitutes for BaseRepository
  - Interface Segregation: concrete repos add only what their domain needs
  - Dependency Inversion: depends on AsyncSession abstraction, not a driver
"""

from __future__ import annotations

from typing import Any, Generic, Optional, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base
from app.core.logging import get_logger

# Bound to Base so the generic type is always an ORM model
ModelType = TypeVar("ModelType", bound=Base)

log = get_logger(__name__)


class BaseRepository(Generic[ModelType]):
    """
    Generic asynchronous repository.

    Provides `get_by_id`, `get_all`, `create`, `update_by_id`,
    `delete_by_id`, `count`, and `exists` operations that work for
    any SQLAlchemy model that has a UUID primary key named `id`.

    Repositories do NOT commit — transaction management is the
    responsibility of the service layer (or the FastAPI dependency
    that owns the session).

    Example:
        class UserRepository(BaseRepository[User]):
            def __init__(self, session: AsyncSession) -> None:
                super().__init__(User, session)

            async def get_by_email(self, email: str) -> User | None:
                result = await self._session.execute(
                    select(User).where(User.email == email)
                )
                return result.scalar_one_or_none()
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    # ── Read ───────────────────────────────────────────────────────────────

    async def get_by_id(self, record_id: UUID) -> Optional[ModelType]:
        """
        Fetch a single record by its UUID primary key.

        Returns None if no record exists with the given ID.
        """
        result = await self._session.execute(
            select(self._model).where(
                self._model.id == record_id  # type: ignore[attr-defined]
            )
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        """
        Return a paginated slice of all records, ordered by insertion order.

        Args:
            skip:  Number of records to skip (offset).
            limit: Maximum number of records to return (default 100).
        """
        result = await self._session.execute(
            select(self._model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def count(self) -> int:
        """Return the total number of records in the table."""
        result = await self._session.execute(
            select(func.count()).select_from(self._model)
        )
        return result.scalar_one()

    async def exists(self, record_id: UUID) -> bool:
        """Return True if a record with the given UUID exists."""
        result = await self._session.execute(
            select(func.count())
            .select_from(self._model)
            .where(self._model.id == record_id)  # type: ignore[attr-defined]
        )
        return result.scalar_one() > 0

    # ── Write ──────────────────────────────────────────────────────────────

    async def create(self, instance: ModelType) -> ModelType:
        """
        Persist a new model instance and flush to assign DB-generated values.

        The caller is responsible for constructing the ORM instance.
        After this method returns, `instance.id` and server defaults
        (e.g. created_at) are populated.

        Does NOT commit — the service layer or request dependency commits.
        """
        self._session.add(instance)
        await self._session.flush()
        await self._session.refresh(instance)
        log.debug(
            f"Created {self._model.__name__}",
            extra={"id": str(getattr(instance, "id", None))},
        )
        return instance

    async def update_by_id(
        self,
        record_id: UUID,
        data: dict[str, Any],
    ) -> Optional[ModelType]:
        """
        Apply a partial update to a record identified by UUID.

        Args:
            record_id: UUID of the record to update.
            data:      Dict of column name → new value.

        Returns the updated record, or None if not found.
        """
        await self._session.execute(
            update(self._model)
            .where(self._model.id == record_id)  # type: ignore[attr-defined]
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        updated = await self.get_by_id(record_id)
        if updated:
            log.debug(
                f"Updated {self._model.__name__}",
                extra={"id": str(record_id), "fields": list(data.keys())},
            )
        return updated

    async def delete_by_id(self, record_id: UUID) -> bool:
        """
        Hard-delete a record by UUID.

        Returns True if a row was deleted, False if not found.
        """
        result = await self._session.execute(
            delete(self._model).where(
                self._model.id == record_id  # type: ignore[attr-defined]
            )
        )
        deleted = result.rowcount > 0
        if deleted:
            log.debug(
                f"Deleted {self._model.__name__}",
                extra={"id": str(record_id)},
            )
        return deleted
