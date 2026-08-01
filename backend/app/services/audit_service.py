"""
DarkTrust – Audit Service

Business logic layer for querying and aggregating audit logs.
Exposes data for admin dashboard monitoring.
"""

from typing import Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.audit_log import AuditLog, AuditEventType, AuditStatus
from app.repositories.audit_repository import AuditRepository

class AuditService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = AuditRepository(session)

    async def get_logs(self, limit: int = 100, skip: int = 0) -> list[AuditLog]:
        """Retrieves a paginated list of audit logs."""
        return await self.repository.get_all(skip=skip, limit=limit)

    async def get_logs_by_user(self, user_id: uuid.UUID) -> list[AuditLog]:
        """Retrieves audit logs filtered by a specific user."""
        stmt = select(AuditLog).where(AuditLog.user_id == user_id).order_by(AuditLog.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_logs_by_event(self, event_type: AuditEventType) -> list[AuditLog]:
        """Retrieves audit logs filtered by a specific event type."""
        stmt = select(AuditLog).where(AuditLog.event_type == event_type).order_by(AuditLog.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_security_summary(self) -> dict[str, Any]:
        """
        Calculates aggregates for an admin dashboard.
        Returns total events, failed logins, and access denied counts.
        """
        # Note: In production, these should be time-bounded (e.g., last 24h)
        total_stmt = select(func.count(AuditLog.id))
        total_result = await self.session.execute(total_stmt)
        total_events = total_result.scalar_one_or_none() or 0

        failed_login_stmt = select(func.count(AuditLog.id)).where(
            AuditLog.event_type == AuditEventType.LOGIN_FAILURE
        )
        failed_login_result = await self.session.execute(failed_login_stmt)
        failed_logins = failed_login_result.scalar_one_or_none() or 0
        
        access_denied_stmt = select(func.count(AuditLog.id)).where(
            AuditLog.event_type == AuditEventType.ACCESS_DENIED
        )
        access_denied_result = await self.session.execute(access_denied_stmt)
        access_denied = access_denied_result.scalar_one_or_none() or 0

        return {
            "total_events": total_events,
            "failed_logins": failed_logins,
            "access_denied": access_denied
        }
