"""
DarkTrust – Zero Trust Security Platform
TrustContext ORM Model

An immutable snapshot of the Zero Trust evaluation performed for a single
HTTP request.  Created by the TrustEvaluatorMiddleware; never updated.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class RiskLevel(str, PyEnum):
    """
    Trust-score tier derived from the computed float score (0–100).

    CRITICAL:  0 – 20   → deny, immediate threat
    LOW:      21 – 40   → high risk, step-up auth recommended
    MEDIUM:   41 – 60   → elevated, monitor closely
    HIGH:     61 – 80   → trusted, normal operation
    VERIFIED: 81 – 100  → verified, highest trust
    """
    CRITICAL = "critical"
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    VERIFIED = "verified"


class TrustContext(Base):
    """
    Per-request Zero Trust evaluation snapshot.

    One record is created for every evaluated request.  The record
    is immutable after creation — no updated_at column intentionally.
    `is_allowed` reflects the final access decision for this request.
    """

    __tablename__ = "trust_contexts"
    __table_args__ = {"comment": "Immutable per-request Zero Trust evaluation snapshots"}

    # ── Primary key ────────────────────────────────────────────────────────
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique trust context identifier (UUIDv4)",
    )

    # ── Request identity ───────────────────────────────────────────────────
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="Authenticated user — NULL for unauthenticated requests",
    )
    request_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="X-Request-ID header value for distributed tracing",
    )
    session_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Session identifier if a session exists",
    )

    # ── Client fingerprint ─────────────────────────────────────────────────
    ip_address: Mapped[str] = mapped_column(
        String(45),       # Supports IPv6 (max 39 chars) + prefix
        nullable=False,
        index=True,
        comment="Client IP address (IPv4 or IPv6)",
    )
    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Raw User-Agent header",
    )
    device_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Device fingerprint (set by the client SDK)",
    )

    # ── Trust evaluation result ────────────────────────────────────────────
    trust_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Computed trust score 0.0 (no trust) – 100.0 (fully verified)",
    )
    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(RiskLevel, name="risk_level_enum"),
        nullable=False,
        comment="Tier derived from trust_score",
    )
    is_allowed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        comment="Final access decision for this request",
    )
    denial_reason: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Machine-readable reason for denial (populated when is_allowed=False)",
    )

    # ── Supplementary context ──────────────────────────────────────────────
    evaluated_policies: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Snapshot of policy IDs evaluated and their outcomes",
    )
    extra_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Additional context (geo-IP, anomaly flags, etc.)",
    )

    # ── Immutable timestamp ────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp of trust evaluation (UTC)",
    )

    # ── Relationships ──────────────────────────────────────────────────────
    user: Mapped[Optional[User]] = relationship(
        "User",
        back_populates="trust_contexts",
        lazy="selectin",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<TrustContext id={self.id!s} "
            f"score={self.trust_score:.1f} "
            f"allowed={self.is_allowed}>"
        )
