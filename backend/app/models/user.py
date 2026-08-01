"""
DarkTrust – Zero Trust Security Platform
User ORM Model

Represents a platform identity with credentials, lifecycle status,
and relationships to roles, audit logs, and trust contexts.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Enum, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user_role import UserRole
    from app.models.audit_log import AuditLog
    from app.models.trust_context import TrustContext


class UserStatus(str, PyEnum):
    """Lifecycle states for a user account."""
    ACTIVE    = "active"
    INACTIVE  = "inactive"
    SUSPENDED = "suspended"
    PENDING   = "pending"


class User(Base, TimestampMixin):
    """
    Platform user account.

    Each user may hold multiple roles (via UserRole), and every
    request they make produces a TrustContext snapshot and an
    AuditLog entry.  The hashed_password field must NEVER store
    plaintext — hashing is the responsibility of the auth service.
    """

    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
        {"comment": "Platform user accounts"},
    )

    # ── Primary key ────────────────────────────────────────────────────────
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique user identifier (UUIDv4)",
    )

    # ── Identity fields ────────────────────────────────────────────────────
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique login username",
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique email address",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Bcrypt-hashed password — never plaintext",
    )
    full_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Optional display name",
    )

    # ── Account flags ──────────────────────────────────────────────────────
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether the account may authenticate",
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Superuser flag — bypasses all policy checks",
    )
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status_enum"),
        default=UserStatus.PENDING,
        nullable=False,
        comment="Current account lifecycle state",
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Timestamp of last successful authentication",
    )

    # ── Relationships ──────────────────────────────────────────────────────
    # user_roles: small collection, always needed — use selectin
    user_roles: Mapped[List[UserRole]] = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # audit_logs / trust_contexts: potentially unbounded — raise on implicit access;
    # always load explicitly via AuditRepository / TrustRepository.
    audit_logs: Mapped[List[AuditLog]] = relationship(
        "AuditLog",
        back_populates="user",
        passive_deletes=True,   # DB handles CASCADE
        lazy="raise",
    )
    trust_contexts: Mapped[List[TrustContext]] = relationship(
        "TrustContext",
        back_populates="user",
        passive_deletes=True,
        lazy="raise",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User id={self.id!s} username={self.username!r} status={self.status}>"
