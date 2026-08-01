"""
DarkTrust – Zero Trust Security Platform
UserRepository

Database operations for the User model.
No business logic — only query construction and execution.
"""

from __future__ import annotations

from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User, UserStatus
from app.models.user_role import UserRole
from app.models.role import Role
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for all User-related database operations.

    Inherits standard CRUD from BaseRepository[User] and adds
    domain-specific finders and relationship-aware queries.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    # ── Finders ────────────────────────────────────────────────────────────

    async def get_by_email(self, email: str) -> Optional[User]:
        """Return the user with a matching email address, or None."""
        result = await self._session.execute(
            select(User).where(User.email == email.lower().strip())
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Return the user with a matching username (case-insensitive), or None."""
        result = await self._session.execute(
            select(User).where(User.username == username.lower().strip())
        )
        return result.scalar_one_or_none()

    # ── Filtered queries ───────────────────────────────────────────────────

    async def get_active_users(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        """Return paginated active (is_active=True, status=ACTIVE) users."""
        result = await self._session.execute(
            select(User)
            .where(User.is_active.is_(True), User.status == UserStatus.ACTIVE)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_status(
        self,
        status: UserStatus,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        """Return paginated users filtered by lifecycle status."""
        result = await self._session.execute(
            select(User)
            .where(User.status == status)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # ── Relationship-aware queries ─────────────────────────────────────────

    async def get_with_roles(self, user_id: UUID) -> Optional[User]:
        """
        Return a user with its user_roles + nested roles eagerly loaded.

        Use this method when you need the user's role list in a single query.
        """
        result = await self._session.execute(
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.user_roles).selectinload(UserRole.role)
            )
        )
        return result.scalar_one_or_none()

    # ── Existence checks ───────────────────────────────────────────────────

    async def email_exists(self, email: str) -> bool:
        """Return True if any user has the given email address."""
        from sqlalchemy import func
        result = await self._session.execute(
            select(func.count())
            .select_from(User)
            .where(User.email == email.lower().strip())
        )
        return result.scalar_one() > 0

    async def username_exists(self, username: str) -> bool:
        """Return True if any user has the given username."""
        from sqlalchemy import func
        result = await self._session.execute(
            select(func.count())
            .select_from(User)
            .where(User.username == username.lower().strip())
        )
        return result.scalar_one() > 0
