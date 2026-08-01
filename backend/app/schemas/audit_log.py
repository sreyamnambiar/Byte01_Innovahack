"""
DarkTrust – AuditLog Pydantic Schemas

Request/response contracts for the immutable security audit trail.
AuditLogs are created internally; they are never created via user-facing API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import Field

from app.models.audit_log import AuditEventType, AuditStatus
from app.schemas.common import DarkTrustBaseModel, ORMBaseModel


class AuditLogBase(DarkTrustBaseModel):
    """Fields common to all AuditLog representations."""

    event_type: AuditEventType
    resource: str = Field(..., max_length=100)
    resource_id: Optional[str] = Field(default=None, max_length=255)
    action: str = Field(..., max_length=50)
    status: AuditStatus
    ip_address: Optional[str] = Field(default=None, max_length=45)
    request_id: Optional[str] = Field(default=None, max_length=100)


class AuditLogCreate(AuditLogBase):
    """
    Schema used internally by AuditService to record an event.
    Not exposed directly as an API endpoint.
    """

    user_id: Optional[UUID] = None
    trust_context_id: Optional[UUID] = None
    user_agent: Optional[str] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = None


class AuditLogResponse(AuditLogBase, ORMBaseModel):
    """AuditLog representation returned by API endpoints."""

    id: UUID
    user_id: Optional[UUID] = None
    trust_context_id: Optional[UUID] = None
    user_agent: Optional[str] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
