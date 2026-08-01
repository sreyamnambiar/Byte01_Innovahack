"""
DarkTrust – Repositories package barrel export.

Usage:
    from app.repositories import UserRepository, AuditRepository
"""

from app.repositories.base import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.policy_repository import PolicyRepository
from app.repositories.audit_repository import AuditRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "RoleRepository",
    "PermissionRepository",
    "PolicyRepository",
    "AuditRepository",
]
