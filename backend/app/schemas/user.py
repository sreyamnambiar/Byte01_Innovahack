"""
DarkTrust – User Pydantic Schemas

Request/response contracts for the User domain.
Passwords are NEVER included in response schemas.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from app.models.user import UserStatus
from app.schemas.common import DarkTrustBaseModel, ORMBaseModel, TimestampSchema


# ── Base ───────────────────────────────────────────────────────────────────

class UserBase(DarkTrustBaseModel):
    """Fields common to create and response schemas."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Unique login username (3–100 characters)",
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address",
    )
    full_name: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional display name",
    )

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """Username may only contain letters, digits, underscores, and hyphens."""
        import re
        if not re.match(r"^[a-zA-Z0-9_\-]+$", v):
            raise ValueError(
                "Username may only contain letters, digits, underscores, and hyphens"
            )
        return v.lower()


# ── Create ─────────────────────────────────────────────────────────────────

class UserCreate(UserBase):
    """Schema used when registering a new user. Includes the plain-text password."""

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plain-text password (min 8 characters) — hashed before storage",
    )


# ── Response ───────────────────────────────────────────────────────────────

class UserResponse(UserBase, TimestampSchema):
    """
    Safe user representation returned by all API endpoints.
    hashed_password is intentionally EXCLUDED.
    """

    id: UUID
    is_active: bool
    is_superuser: bool
    status: UserStatus
    last_login_at: Optional[datetime] = None


class UserSummary(ORMBaseModel):
    """Minimal user projection used in nested responses (e.g., inside AuditLog)."""

    id: UUID
    username: str
    email: str
    full_name: Optional[str] = None
    status: UserStatus
