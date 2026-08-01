"""
DarkTrust – Zero Trust Security Platform
AuditRepository

Database operations for the AuditLog model.
Records are append-only — create is supported, update/delete are NOT.
No business logic — only query construction and execution.
"""

from __future__ import annotations

from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog, AuditEventType, AuditStatus
from app.repositories.base import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    """
    Repository for the immutable AuditLog model.

    Inherits `create` and `get_by_id` from BaseRepository[AuditLog].
    `update_by_id` and `delete_by_id` are intentionally NOT overridden —
    the inherited versions exist for framework completeness, but the
    service layer MUST NEVER call them for audit records.

    Domain-specific read queries support the Audit Log API and the
    security dashboard.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AuditLog, session)

    # ── User-scoped queries ────────────────────────────────────────────────

    async def get_by_user_id(
        self,
        user_id: UUID,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[AuditLog]:
        """Return paginated audit logs for a specific user, newest first."""
        result = await self._session.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def count_by_user(self, user_id: UUID) -> int:
        """Return the total number of audit events for a specific user."""
        from sqlalchemy import func
        result = await self._session.execute(
            select(func.count())
            .select_from(AuditLog)
            .where(AuditLog.user_id == user_id)
        )
        return result.scalar_one()

    # ── Request tracing ────────────────────────────────────────────────────

    async def get_by_request_id(self, request_id: str) -> Sequence[AuditLog]:
        """
        Return all audit events associated with a specific X-Request-ID.

        A single request may produce multiple audit events (e.g. access
        check + subsequent DB operation), hence a list is returned.
        """
        result = await self._session.execute(
            select(AuditLog)
            .where(AuditLog.request_id == request_id)
            .order_by(AuditLog.created_at.asc())
        )
        return result.scalars().all()

    # ── Event classification queries ───────────────────────────────────────

    async def get_by_event_type(
        self,
        event_type: AuditEventType,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[AuditLog]:
        """Return paginated logs filtered by event type, newest first."""
        result = await self._session.execute(
            select(AuditLog)
            .where(AuditLog.event_type == event_type)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_status(
        self,
        status: AuditStatus,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[AuditLog]:
        """Return paginated logs filtered by outcome status, newest first."""
        result = await self._session.execute(
            select(AuditLog)
            .where(AuditLog.status == status)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_denied_events(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[AuditLog]:
        """Return recent access-denied events — used by the security dashboard."""
        result = await self._session.execute(
            select(AuditLog)
            .where(AuditLog.status == AuditStatus.DENIED)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # ── Resource-scoped queries ────────────────────────────────────────────

    async def get_by_resource(
        self,
        resource: str,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[AuditLog]:
        """Return paginated logs for a specific resource type."""
        result = await self._session.execute(
            select(AuditLog)
            .where(AuditLog.resource == resource)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    # ── Recency query ──────────────────────────────────────────────────────

    async def get_recent(self, *, limit: int = 50) -> Sequence[AuditLog]:
        """
        Return the most recent audit events across all users and resources.

        Used by the security operations dashboard for live feed.
        """
        result = await self._session.execute(
            select(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    # ── IP-based threat queries ────────────────────────────────────────────

    async def get_by_ip_address(
        self,
        ip_address: str,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[AuditLog]:
        """Return paginated logs originating from a specific IP address."""
        result = await self._session.execute(
            select(AuditLog)
            .where(AuditLog.ip_address == ip_address)
            .order_by(AuditLog.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def count_failures_by_ip(self, ip_address: str) -> int:
        """
        Count total FAILURE/DENIED events from a given IP.

        Used by the Rate Limiter and Attack Detector to identify
        brute-force or scanning behaviour.
        """
        from sqlalchemy import func
        result = await self._session.execute(
            select(func.count())
            .select_from(AuditLog)
            .where(
                AuditLog.ip_address == ip_address,
                AuditLog.status.in_([AuditStatus.FAILURE, AuditStatus.DENIED]),
            )
        )
        return result.scalar_one()
