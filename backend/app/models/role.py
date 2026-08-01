"""
DarkTrust – Zero Trust Security Platform
Role ORM Model

A role groups a set of permissions and can be assigned to multiple users.
Implements the Role side of Role-Based Access Control (RBAC).
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user_role import UserRole
    from app.models.role_permission import RolePermission


class Role(Base, TimestampMixin):
    """
    Access control role.

    Roles aggregate permissions and are assigned to users via UserRole.
    A user may hold many roles; roles may grant many permissions.
    """

    __tablename__ = "roles"
    __table_args__ = {"comment": "Named access-control roles"}

    # ── Primary key ────────────────────────────────────────────────────────
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique role identifier (UUIDv4)",
    )

    # ── Role definition ────────────────────────────────────────────────────
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique machine-readable role name (e.g. admin, analyst)",
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Human-readable description of role purpose",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Inactive roles deny all access without deletion",
    )

    # ── Relationships ──────────────────────────────────────────────────────
    # role_permissions: usually small — load with selectin
    role_permissions: Mapped[List[RolePermission]] = relationship(
        "RolePermission",
        back_populates="role",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # user_roles: could be large — raise; load explicitly when needed
    user_roles: Mapped[List[UserRole]] = relationship(
        "UserRole",
        back_populates="role",
        passive_deletes=True,
        lazy="raise",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Role id={self.id!s} name={self.name!r}>"
