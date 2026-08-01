"""
DarkTrust – Zero Trust Security Platform
RoleRepository

Database operations for the Role model and its UserRole/RolePermission associations.
No business logic — only query construction and execution.
"""

from __future__ import annotations

from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """
    Repository for all Role-related database operations.

    Inherits standard CRUD from BaseRepository[Role] and adds
    permission assignment/revocation and relationship queries.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Role, session)

    # ── Finders ────────────────────────────────────────────────────────────

    async def get_by_name(self, name: str) -> Optional[Role]:
        """Return the role with the given machine-readable name, or None."""
        result = await self._session.execute(
            select(Role).where(Role.name == name.lower().strip())
        )
        return result.scalar_one_or_none()

    async def get_active_roles(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Role]:
        """Return paginated active roles."""
        result = await self._session.execute(
            select(Role)
            .where(Role.is_active.is_(True))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # ── Relationship-aware queries ─────────────────────────────────────────

    async def get_with_permissions(self, role_id: UUID) -> Optional[Role]:
        """
        Return a role with its role_permissions + nested permissions loaded.

        Use this when rendering the full permission list for a role.
        """
        result = await self._session.execute(
            select(Role)
            .where(Role.id == role_id)
            .options(
                selectinload(Role.role_permissions).selectinload(RolePermission.permission)
            )
        )
        return result.scalar_one_or_none()

    # ── Association operations ─────────────────────────────────────────────

    async def assign_permission(
        self,
        role_id: UUID,
        permission_id: UUID,
    ) -> RolePermission:
        """
        Grant a permission to a role.

        Creates a RolePermission record.  The DB composite PK constraint
        prevents duplicate grants — this method will raise IntegrityError
        if the grant already exists; the service layer must handle that.
        """
        grant = RolePermission(role_id=role_id, permission_id=permission_id)
        self._session.add(grant)
        await self._session.flush()
        return grant

    async def revoke_permission(
        self,
        role_id: UUID,
        permission_id: UUID,
    ) -> bool:
        """
        Revoke a permission from a role.

        Returns True if a row was deleted, False if the grant did not exist.
        """
        result = await self._session.execute(
            delete(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
        )
        return result.rowcount > 0

    async def assign_to_user(
        self,
        user_id: UUID,
        role_id: UUID,
        assigned_by: Optional[UUID] = None,
    ) -> UserRole:
        """
        Assign this role to a user.

        Creates a UserRole record.  Raises IntegrityError if already assigned;
        the service layer must handle that case.
        """
        assignment = UserRole(
            user_id=user_id,
            role_id=role_id,
            assigned_by=assigned_by,
        )
        self._session.add(assignment)
        await self._session.flush()
        return assignment

    async def revoke_from_user(self, user_id: UUID, role_id: UUID) -> bool:
        """
        Remove a role assignment from a user.

        Returns True if the assignment existed and was removed.
        """
        result = await self._session.execute(
            delete(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
            )
        )
        return result.rowcount > 0

    # ── Existence check ────────────────────────────────────────────────────

    async def name_exists(self, name: str) -> bool:
        """Return True if a role with the given name already exists."""
        from sqlalchemy import func
        result = await self._session.execute(
            select(func.count())
            .select_from(Role)
            .where(Role.name == name.lower().strip())
        )
        return result.scalar_one() > 0
