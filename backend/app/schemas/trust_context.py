"""
DarkTrust – TrustContext Pydantic Schemas

Request/response contracts for Zero Trust evaluation snapshots.
These records are created by the middleware and are read-only via API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import Field

from app.models.trust_context import RiskLevel
from app.schemas.common import DarkTrustBaseModel, ORMBaseModel


class TrustContextBase(DarkTrustBaseModel):
    """Fields common to all TrustContext representations."""

    request_id: str = Field(
        ...,
        max_length=100,
        description="X-Request-ID for distributed tracing",
    )
    session_id: Optional[str] = Field(
        default=None,
        max_length=255,
    )
    ip_address: str = Field(
        ...,
        max_length=45,
        description="Client IP address (IPv4 or IPv6)",
    )
    user_agent: Optional[str] = Field(default=None)
    device_id: Optional[str] = Field(default=None, max_length=255)
    trust_score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Computed trust score — 0.0 (deny) to 100.0 (verified)",
    )
    risk_level: RiskLevel
    is_allowed: bool
    denial_reason: Optional[str] = Field(default=None, max_length=500)


class TrustContextCreate(TrustContextBase):
    """Schema used internally when the TrustEvaluatorMiddleware creates a snapshot."""
    user_id: Optional[UUID] = None
    evaluated_policies: Optional[Dict[str, Any]] = None
    extra_metadata: Optional[Dict[str, Any]] = None


class TrustContextResponse(TrustContextBase, ORMBaseModel):
    """TrustContext representation returned by API endpoints."""
    id: UUID
    user_id: Optional[UUID] = None
    evaluated_policies: Optional[Dict[str, Any]] = None
    extra_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
