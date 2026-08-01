"""
DarkTrust – Zero Trust Security Platform
PolicyRepository

Database operations for the Policy model.
No business logic — only query construction and execution.
The Policy Engine (app/security/policy_engine.py) uses this repository
to load policies for evaluation.
"""

from __future__ import annotations

from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.policy import Policy, PolicyEffect
from app.repositories.base import BaseRepository


class PolicyRepository(BaseRepository[Policy]):
    """
    Repository for all Policy-related database operations.

    Inherits standard CRUD from BaseRepository[Policy] and adds
    resource/action scoped finders that the Policy Engine requires.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Policy, session)

    # ── Finders ────────────────────────────────────────────────────────────

    async def get_by_name(self, name: str) -> Optional[Policy]:
        """Return the policy with the given unique name, or None."""
        result = await self._session.execute(
            select(Policy).where(Policy.name == name)
        )
        return result.scalar_one_or_none()

    async def get_active_policies(
        self,
        *,
        skip: int = 0,
        limit: int = 500,
    ) -> Sequence[Policy]:
        """
        Return all active policies ordered by priority (highest first).

        Used by the Policy Engine to build its evaluation set.
        The default limit is 500 — tune as needed for your policy count.
        """
        result = await self._session.execute(
            select(Policy)
            .where(Policy.is_active.is_(True))
            .order_by(Policy.priority.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_resource(
        self,
        resource: str,
        *,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 200,
    ) -> Sequence[Policy]:
        """
        Return policies that match a given resource, ordered by priority.

        Args:
            resource:    Resource name (exact match or '*').
            active_only: When True, exclude inactive policies.
        """
        stmt = (
            select(Policy)
            .where(Policy.resource.in_([resource, "*"]))
            .order_by(Policy.priority.desc())
            .offset(skip)
            .limit(limit)
        )
        if active_only:
            stmt = stmt.where(Policy.is_active.is_(True))

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_resource_action(
        self,
        resource: str,
        action: str,
        *,
        active_only: bool = True,
    ) -> Sequence[Policy]:
        """
        Return policies that match a resource-action pair, ordered by priority.

        Includes wildcard ('*') matches for both resource and action.
        """
        stmt = (
            select(Policy)
            .where(
                Policy.resource.in_([resource, "*"]),
                Policy.action.in_([action, "*"]),
            )
            .order_by(Policy.priority.desc())
        )
        if active_only:
            stmt = stmt.where(Policy.is_active.is_(True))

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_effect(
        self,
        effect: PolicyEffect,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Policy]:
        """Return all policies with a given effect (ALLOW or DENY)."""
        result = await self._session.execute(
            select(Policy)
            .where(Policy.effect == effect)
            .order_by(Policy.priority.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_creator(
        self,
        created_by: UUID,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Policy]:
        """Return all policies created by a specific user."""
        result = await self._session.execute(
            select(Policy)
            .where(Policy.created_by == created_by)
            .order_by(Policy.priority.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # ── Existence check ────────────────────────────────────────────────────

    async def name_exists(self, name: str) -> bool:
        """Return True if a policy with the given name already exists."""
        from sqlalchemy import func
        result = await self._session.execute(
            select(func.count())
            .select_from(Policy)
            .where(Policy.name == name)
        )
        return result.scalar_one() > 0
