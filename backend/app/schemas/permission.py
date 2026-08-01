"""
DarkTrust – Permission Pydantic Schemas

Request/response contracts for the Permission domain.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import Field, field_validator

from app.schemas.common import DarkTrustBaseModel, TimestampSchema


class PermissionBase(DarkTrustBaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Unique identifier in format resource:action (e.g. users:read)",
    )
    resource: str = Field(
        ...,
        max_length=100,
        description="Target resource (e.g. users, policies, audit_logs, *)",
    )
    action: str = Field(
        ...,
        max_length=50,
        description="Allowed action (e.g. read, write, delete, *)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Human-readable explanation of what this permission allows",
    )

    @field_validator("resource", "action")
    @classmethod
    def lowercase_slug(cls, v: str) -> str:
        """Resource and action must be lowercase slugs or '*'."""
        import re
        if v != "*" and not re.match(r"^[a-z0-9_]+$", v):
            raise ValueError("Must be a lowercase slug (a-z, 0-9, _) or '*'")
        return v


class PermissionCreate(PermissionBase):
    """Schema used when creating a new permission."""
    pass


class PermissionResponse(PermissionBase, TimestampSchema):
    """Permission representation returned by API endpoints."""
    id: UUID
