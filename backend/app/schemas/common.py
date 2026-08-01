"""
DarkTrust – Shared Schema Utilities

Common Pydantic base models and reusable types used across all schema modules.
"""

from __future__ import annotations

from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict

DataType = TypeVar("DataType")


class DarkTrustBaseModel(BaseModel):
    """
    Root Pydantic base for all DarkTrust schemas.

    Configures:
    - populate_by_name: allows both alias and field-name population
    - str_strip_whitespace: auto-strips leading/trailing whitespace
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class ORMBaseModel(DarkTrustBaseModel):
    """
    Base schema for models that are read from the database (ORM mode).

    All Response schemas inherit from this so SQLAlchemy ORM objects
    can be passed directly to Pydantic without conversion.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,     # Enable ORM mode (Pydantic v2)
    )


class PaginatedResponse(BaseModel, Generic[DataType]):
    """
    Generic paginated response wrapper.

    Usage:
        PaginatedResponse[UserResponse](items=[...], total=10, skip=0, limit=20)
    """

    items: List[DataType]
    total: int
    skip: int
    limit: int
    has_more: bool

    @classmethod
    def build(
        cls,
        items: List[DataType],
        total: int,
        skip: int,
        limit: int,
    ) -> "PaginatedResponse[DataType]":
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + len(items)) < total,
        )


class TimestampSchema(ORMBaseModel):
    """Mixin that adds created_at / updated_at to response schemas."""

    created_at: datetime
    updated_at: Optional[datetime] = None
