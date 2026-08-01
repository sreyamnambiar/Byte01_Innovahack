"""
DarkTrust – Policy Pydantic Schemas

Request/response contracts for the Zero Trust Policy domain.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import Field

from app.models.policy import PolicyEffect
from app.schemas.common import DarkTrustBaseModel, TimestampSchema


class PolicyBase(DarkTrustBaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Unique policy name",
    )
    description: Optional[str] = Field(
        default=None,
        description="Human-readable description of what this policy does",
    )
    resource: str = Field(
        ...,
        max_length=100,
        description="Target resource path or wildcard (e.g. users, policies, *)",
    )
    action: str = Field(
        ...,
        max_length=50,
        description="Target action or wildcard (e.g. read, write, delete, *)",
    )
    effect: PolicyEffect = Field(
        default=PolicyEffect.DENY,
        description="Whether this policy ALLOW or DENY access",
    )
    conditions: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional JSONB conditions evaluated by the Policy Engine",
    )
    priority: int = Field(
        default=0,
        ge=0,
        le=10000,
        description="Evaluation priority — higher value = evaluated first",
    )
    is_active: bool = Field(
        default=True,
        description="Inactive policies are skipped during evaluation",
    )


class PolicyCreate(PolicyBase):
    """Schema used when creating a new policy."""
    pass


class PolicyResponse(PolicyBase, TimestampSchema):
    """Policy representation returned by API endpoints."""
    id: UUID
    created_by: Optional[UUID] = None
