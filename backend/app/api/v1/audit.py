"""
DarkTrust – Audit API Router

Exposes REST endpoints for querying the Security Audit Log.
Restricted to administrators.
"""

from typing import Any
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.audit_log import AuditEventType
from app.services.audit_service import AuditService
from app.auth.dependencies import require_role

router = APIRouter(
    prefix="/audit", 
    tags=["Audit Logs"],
    dependencies=[Depends(require_role("admin"))]
)


def get_audit_service(session: AsyncSession = Depends(get_db)) -> AuditService:
    return AuditService(session)


@router.get(
    "/logs",
    summary="List audit logs",
    description="Retrieves a paginated list of all security audit logs."
)
async def list_audit_logs(
    limit: int = 100, 
    skip: int = 0,
    audit_service: AuditService = Depends(get_audit_service)
) -> list[Any]:
    logs = await audit_service.get_logs(limit=limit, skip=skip)
    return logs


@router.get(
    "/users/{user_id}",
    summary="Get audit logs by user",
    description="Retrieves all security events triggered by a specific user."
)
async def list_audit_logs_by_user(
    user_id: uuid.UUID,
    audit_service: AuditService = Depends(get_audit_service)
) -> list[Any]:
    logs = await audit_service.get_logs_by_user(user_id)
    return logs


@router.get(
    "/events/{event_type}",
    summary="Get audit logs by event type",
    description="Retrieves all logs matching a specific event classification."
)
async def list_audit_logs_by_event(
    event_type: AuditEventType,
    audit_service: AuditService = Depends(get_audit_service)
) -> list[Any]:
    logs = await audit_service.get_logs_by_event(event_type)
    return logs


@router.get(
    "/security-summary",
    summary="Get Security Dashboard Summary",
    description="Aggregates security events for the admin monitoring dashboard."
)
async def get_security_summary(
    audit_service: AuditService = Depends(get_audit_service)
) -> dict[str, Any]:
    return await audit_service.get_security_summary()
