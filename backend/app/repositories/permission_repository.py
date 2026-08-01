"""
DarkTrust – Zero Trust Security Platform
PermissionRepository

Database operations for the Permission model.
No business logic — only query construction and execution.
"""

from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    """
    Repository for all Permission-related database operations.

    Inherits standard CRUD from BaseRepository[Permission] and adds
    resource/action based finders.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Permission, session)

    # ── Finders ────────────────────────────────────────────────────────────

    async def get_by_name(self, name: str) -> Optional[Permission]:
        """Return the permission with the given unique name, or None."""
        result = await self._session.execute(
            select(Permission).where(Permission.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_resource_action(
        self,
        resource: str,
        action: str,
    ) -> Optional[Permission]:
        """
        Return the permission that covers a specific resource-action pair.

        Exact match only — wildcard resolution is the Policy Engine's job.
        """
        result = await self._session.execute(
            select(Permission).where(
                Permission.resource == resource,
                Permission.action == action,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_resource(
        self,
        resource: str,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Permission]:
        """Return all permissions for a given resource."""
        result = await self._session.execute(
            select(Permission)
            .where(Permission.resource == resource)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # ── Existence check ────────────────────────────────────────────────────

    async def name_exists(self, name: str) -> bool:
        """Return True if a permission with the given name already exists."""
        from sqlalchemy import func
        result = await self._session.execute(
            select(func.count())
            .select_from(Permission)
            .where(Permission.name == name)
        )
        return result.scalar_one() > 0

    async def resource_action_exists(self, resource: str, action: str) -> bool:
        """Return True if a permission for this resource-action already exists."""
        from sqlalchemy import func
        result = await self._session.execute(
            select(func.count())
            .select_from(Permission)
            .where(
                Permission.resource == resource,
                Permission.action == action,
            )
        )
        return result.scalar_one() > 0
