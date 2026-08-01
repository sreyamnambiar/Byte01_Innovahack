"""
DarkTrust – Zero Trust Security Platform
UserRole Association Model

Maps users to roles. Uses a composite primary key (user_id, role_id)
to enforce uniqueness at the database level.
Tracks who assigned the role and when.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.role import Role


class UserRole(Base):
    """
    User ↔ Role many-to-many association.

    Composite PK (user_id, role_id) prevents duplicate assignments.
    'assigned_by' records which admin granted the role.
    This is an immutable record — role changes appear as delete + insert.
    """

    __tablename__ = "user_roles"
    __table_args__ = {"comment": "User-to-role assignments"}

    # ── Composite primary key ──────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        comment="FK → users.id",
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
        comment="FK → roles.id",
    )

    # ── Assignment metadata ────────────────────────────────────────────────
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="User who performed this role assignment",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the role was assigned (UTC)",
    )

    # ── Relationships ──────────────────────────────────────────────────────
    user: Mapped[User] = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="user_roles",
        lazy="selectin",
    )
    role: Mapped[Role] = relationship(
        "Role",
        foreign_keys=[role_id],
        back_populates="user_roles",
        lazy="selectin",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<UserRole user={self.user_id!s} role={self.role_id!s}>"
