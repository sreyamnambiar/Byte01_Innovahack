"""
DarkTrust – Zero Trust Security Platform
RolePermission Association Model

Maps roles to permissions. Composite PK enforces uniqueness.
Immutable records — changes are delete + insert.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.permission import Permission


class RolePermission(Base):
    """
    Role ↔ Permission many-to-many association.

    Composite PK (role_id, permission_id) prevents duplicate grants.
    Deletion of a Role cascades and removes all its grants.
    """

    __tablename__ = "role_permissions"
    __table_args__ = {"comment": "Role-to-permission grants"}

    # ── Composite primary key ──────────────────────────────────────────────
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
        comment="FK → roles.id",
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
        comment="FK → permissions.id",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the permission was granted (UTC)",
    )

    # ── Relationships ──────────────────────────────────────────────────────
    role: Mapped[Role] = relationship(
        "Role",
        back_populates="role_permissions",
        lazy="selectin",
    )
    permission: Mapped[Permission] = relationship(
        "Permission",
        back_populates="role_permissions",
        lazy="selectin",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<RolePermission role={self.role_id!s} permission={self.permission_id!s}>"
