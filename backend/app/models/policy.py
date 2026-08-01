"""
DarkTrust – Zero Trust Security Platform
Policy ORM Model

Defines an Attribute-Based Access Control (ABAC) policy that allows or
denies access to a resource-action pair under optional conditions.
The Zero Trust Policy Engine evaluates these records at request time.
"""

from __future__ import annotations

import uuid
from enum import Enum as PyEnum
from typing import Any, Optional

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class PolicyEffect(str, PyEnum):
    """Whether the policy grants or denies access."""
    ALLOW = "allow"
    DENY  = "deny"


class Policy(Base, TimestampMixin):
    """
    Zero Trust access-control policy.

    Evaluated by the Policy Engine for every protected request.
    Higher-priority policies take precedence when multiple policies match.
    DENY always overrides ALLOW at the same priority level.

    `conditions` is a JSONB field that stores arbitrary contextual
    constraints (e.g. IP ranges, time windows, device type).  The
    Policy Engine is responsible for interpreting them.
    """

    __tablename__ = "policies"
    __table_args__ = {"comment": "Zero Trust ABAC access control policies"}

    # ── Primary key ────────────────────────────────────────────────────────
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique policy identifier (UUIDv4)",
    )

    # ── Policy identity ────────────────────────────────────────────────────
    name: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique policy name",
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Human-readable description of what this policy does",
    )

    # ── Scope ─────────────────────────────────────────────────────────────
    resource: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        comment="Target resource path or wildcard (e.g. users, policies, *)",
    )
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Target action or wildcard (e.g. read, write, delete, *)",
    )

    # ── Decision ──────────────────────────────────────────────────────────
    effect: Mapped[PolicyEffect] = mapped_column(
        Enum(PolicyEffect, name="policy_effect_enum"),
        default=PolicyEffect.DENY,
        nullable=False,
        comment="Whether this policy grants or denies access",
    )
    conditions: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Optional JSONB conditions evaluated by the Policy Engine",
    )
    priority: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        index=True,
        comment="Evaluation priority — higher value = evaluated first",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Inactive policies are skipped during evaluation",
    )

    # ── Provenance ────────────────────────────────────────────────────────
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="User who created this policy",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Policy id={self.id!s} name={self.name!r} effect={self.effect}>"
