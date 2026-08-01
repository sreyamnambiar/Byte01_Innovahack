"""
DarkTrust – Role Pydantic Schemas

Request/response contracts for the Role domain.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import Field

from app.schemas.common import DarkTrustBaseModel, TimestampSchema


class RoleBase(DarkTrustBaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Unique machine-readable role name (e.g. admin, analyst)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Human-readable description of this role's purpose",
    )


class RoleCreate(RoleBase):
    """Schema used when creating a new role."""
    pass


class RoleResponse(RoleBase, TimestampSchema):
    """Role representation returned by API endpoints."""
    id: UUID
    is_active: bool
