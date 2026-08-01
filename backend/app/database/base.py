"""
DarkTrust – Zero Trust Security Platform
SQLAlchemy Declarative Base

All ORM models must inherit from this Base class.
This module is intentionally minimal — models are defined in app/models/.
"""

from sqlalchemy.orm import DeclarativeBase, MappedColumn, mapped_column
from sqlalchemy import DateTime, func
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    """
    Abstract SQLAlchemy declarative base for all DarkTrust ORM models.

    All database models must inherit from this class.
    Provides a consistent foundation for table mapping.

    Example:
        class User(Base):
            __tablename__ = "users"
            id: Mapped[int] = mapped_column(primary_key=True)
    """
    pass


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at timestamp columns.

    Apply to any model that requires audit timestamps.
    SQLAlchemy server-side defaults ensure accuracy regardless
    of application-layer time zone settings.

    Usage:
        class User(Base, TimestampMixin):
            __tablename__ = "users"
            ...
    """

    created_at: MappedColumn[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp (UTC)",
    )

    updated_at: MappedColumn[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="Record last update timestamp (UTC)",
    )
