"""
DarkTrust – Security Events

Defines the Pydantic schemas for standardizing audit log payloads 
before they are written to the database by the AuditLogger.
"""

from typing import Any
from pydantic import BaseModel, Field
import uuid
from app.models.audit_log import AuditEventType, AuditStatus

class BaseEventPayload(BaseModel):
    user_id: uuid.UUID | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    resource: str = "system"
    resource_id: str | None = None
    action: str
    status: AuditStatus = AuditStatus.SUCCESS
    error_message: str | None = None
    extra_metadata: dict[str, Any] | None = None

class AuthenticationEvent(BaseEventPayload):
    """Payload for login, logout, and token refresh events."""
    pass

class AuthorizationEvent(BaseEventPayload):
    """Payload for RBAC assignments (roles, permissions)."""
    old_values: dict[str, Any] | None = None
    new_values: dict[str, Any] | None = None

class PolicyEvaluationEvent(BaseEventPayload):
    """Payload for Zero Trust Policy Engine decisions."""
    request_id: str | None = None
    trust_context_id: uuid.UUID | None = None
    old_values: dict[str, Any] | None = None
    new_values: dict[str, Any] | None = None
