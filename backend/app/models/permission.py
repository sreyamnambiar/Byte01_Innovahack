"""
DarkTrust – Zero Trust Security Platform
Permission ORM Model

A granular, resource-action access right that is assigned to roles.
Follows the pattern: subject (Role) → permission → resource:action.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.role_permission import RolePermission


class Permission(Base, TimestampMixin):
    """
    Granular access permission.

    A permission combines a resource and an action into a single
    access right.  Permissions are assigned to roles, and roles are
    assigned to users.

    Examples:
        resource="policies",  action="read"
        resource="users",     action="delete"
        resource="audit_logs",action="export"
    """

    __tablename__ = "permissions"
    __table_args__ = (
        UniqueConstraint("resource", "action", name="uq_permission_resource_action"),
        {"comment": "Granular resource-action access rights"},
    )

    # ── Primary key ────────────────────────────────────────────────────────
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique permission identifier (UUIDv4)",
    )

    # ── Permission definition ──────────────────────────────────────────────
    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique human-readable identifier (e.g. policies:read)",
    )
    resource: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Target resource (e.g. users, policies, audit_logs, *)",
    )
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Allowed action (e.g. read, write, delete, *)",
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Human-readable explanation of this permission",
    )

    # ── Relationships ──────────────────────────────────────────────────────
    role_permissions: Mapped[List[RolePermission]] = relationship(
        "RolePermission",
        back_populates="permission",
        passive_deletes=True,
        lazy="raise",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Permission id={self.id!s} name={self.name!r}>"
