"""
DarkTrust – Schemas package barrel export.

Import from here for a clean, single-source import path.

Usage:
    from app.schemas import UserCreate, UserResponse, PolicyCreate
"""

from app.schemas.common import (
    DarkTrustBaseModel,
    ORMBaseModel,
    PaginatedResponse,
    TimestampSchema,
)
from app.schemas.user import UserBase, UserCreate, UserResponse, UserSummary
from app.schemas.role import RoleBase, RoleCreate, RoleResponse
from app.schemas.permission import PermissionBase, PermissionCreate, PermissionResponse
from app.schemas.policy import PolicyBase, PolicyCreate, PolicyResponse
from app.schemas.trust_context import (
    TrustContextBase,
    TrustContextCreate,
    TrustContextResponse,
)
from app.schemas.audit_log import AuditLogBase, AuditLogCreate, AuditLogResponse
from app.schemas.token import Token, RefreshTokenRequest

__all__ = [
    # Common
    "DarkTrustBaseModel",
    "ORMBaseModel",
    "PaginatedResponse",
    "TimestampSchema",
    # User
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserSummary",
    # Role
    "RoleBase",
    "RoleCreate",
    "RoleResponse",
    # Permission
    "PermissionBase",
    "PermissionCreate",
    "PermissionResponse",
    # Policy
    "PolicyBase",
    "PolicyCreate",
    "PolicyResponse",
    # TrustContext
    "TrustContextBase",
    "TrustContextCreate",
    "TrustContextResponse",
    # AuditLog
    "AuditLogBase",
    "AuditLogCreate",
    "AuditLogResponse",
    # Token
    "Token",
    "RefreshTokenRequest",
]
