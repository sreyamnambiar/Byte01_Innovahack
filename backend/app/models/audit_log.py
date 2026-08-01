"""
DarkTrust – Zero Trust Security Platform
AuditLog ORM Model

Tamper-evident, immutable record of every significant security event.
Never updated after creation — append-only log.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AuditEventType(str, PyEnum):
    """Taxonomy of auditable platform events."""
    # Authentication events
    LOGIN_SUCCESS        = "login_success"
    LOGIN_FAILURE        = "login_failure"
    LOGOUT               = "logout"
    TOKEN_REFRESH        = "token_refresh"
    TOKEN_REVOKED        = "token_revoked"

    # Access decisions
    ACCESS_GRANTED       = "access_granted"
    ACCESS_DENIED        = "access_denied"
    POLICY_VIOLATION     = "policy_violation"

    # Administrative actions
    USER_CREATED         = "user_created"
    USER_UPDATED         = "user_updated"
    USER_DELETED         = "user_deleted"
    USER_SUSPENDED       = "user_suspended"
    ROLE_ASSIGNED        = "role_assigned"
    ROLE_REVOKED         = "role_revoked"
    PERMISSION_GRANTED   = "permission_granted"
    PERMISSION_REVOKED   = "permission_revoked"

    # Policy management
    POLICY_CREATED       = "policy_created"
    POLICY_UPDATED       = "policy_updated"
    POLICY_DELETED       = "policy_deleted"

    # Security events
    SUSPICIOUS_ACTIVITY  = "suspicious_activity"
    RATE_LIMIT_EXCEEDED  = "rate_limit_exceeded"
    ATTACK_DETECTED      = "attack_detected"

    # System events
    SYSTEM_STARTUP       = "system_startup"
    SYSTEM_SHUTDOWN      = "system_shutdown"
    CONFIG_CHANGED       = "config_changed"


class AuditStatus(str, PyEnum):
    """Outcome of the audited action."""
    SUCCESS = "success"
    FAILURE = "failure"
    DENIED  = "denied"
    ERROR   = "error"


class AuditLog(Base):
    """
    Security event audit record.

    Append-only — records are NEVER updated.  All DB-level constraints
    enforce this by omitting updated_at and by SET NULL on the user FK
    (preserving the audit trail even after user deletion).

    'old_values' / 'new_values' record the before/after state for
    mutation events (user update, policy change, etc.).
    """

    __tablename__ = "audit_logs"
    __table_args__ = {"comment": "Immutable security-event audit trail"}

    # ── Primary key ────────────────────────────────────────────────────────
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique audit log entry identifier (UUIDv4)",
    )

    # ── Actor ─────────────────────────────────────────────────────────────
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="User who triggered the event — NULL for system events",
    )

    # ── Request tracing ────────────────────────────────────────────────────
    request_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="X-Request-ID for cross-service tracing",
    )
    trust_context_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("trust_contexts.id", ondelete="SET NULL"),
        nullable=True,
        comment="Associated trust evaluation snapshot",
    )

    # ── Event details ──────────────────────────────────────────────────────
    event_type: Mapped[AuditEventType] = mapped_column(
        Enum(AuditEventType, name="audit_event_type_enum"),
        nullable=False,
        index=True,
        comment="Classification of the audited event",
    )
    resource: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Resource type affected (e.g. users, policies)",
    )
    resource_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Specific resource instance identifier",
    )
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Action attempted (e.g. read, write, delete)",
    )
    status: Mapped[AuditStatus] = mapped_column(
        Enum(AuditStatus, name="audit_status_enum"),
        nullable=False,
        index=True,
        comment="Outcome of the action",
    )

    # ── Client context ─────────────────────────────────────────────────────
    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
        comment="Client IP address at time of event",
    )
    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Client User-Agent at time of event",
    )

    # ── Mutation payloads ──────────────────────────────────────────────────
    old_values: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="State of the resource BEFORE the action (mutations only)",
    )
    new_values: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="State of the resource AFTER the action (mutations only)",
    )

    # ── Additional context ─────────────────────────────────────────────────
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Error message if the action resulted in FAILURE or ERROR",
    )
    extra_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Additional structured context (geo, threat flags, etc.)",
    )

    # ── Immutable timestamp ────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        comment="Event timestamp (UTC) — immutable after insert",
    )

    # ── Relationships ──────────────────────────────────────────────────────
    user: Mapped[Optional[User]] = relationship(
        "User",
        back_populates="audit_logs",
        lazy="selectin",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<AuditLog id={self.id!s} "
            f"event={self.event_type} "
            f"status={self.status}>"
        )
