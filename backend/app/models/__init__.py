"""
DarkTrust – Models package.

Importing every model here has two effects:
  1. They are registered in Base.metadata, enabling Alembic autogenerate.
  2. They are importable from `app.models` with a single import.

Import ORDER matters — leaf models (no FK dependencies) first,
then association tables, then models that reference them.

RULE: Every new model MUST be added to this file before running migrations.
"""

# ── Independent models (no FK to each other) ──────────────────────────────
from app.models.user import User, UserStatus  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.permission import Permission  # noqa: F401

# ── Association models (depend on User, Role, Permission) ──────────────────
from app.models.user_role import UserRole  # noqa: F401
from app.models.role_permission import RolePermission  # noqa: F401

# ── Security & audit models ────────────────────────────────────────────────
from app.models.policy import Policy, PolicyEffect  # noqa: F401
from app.models.trust_context import TrustContext, RiskLevel  # noqa: F401
from app.models.audit_log import AuditLog, AuditEventType, AuditStatus  # noqa: F401

__all__ = [
    # Models
    "User",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    "Policy",
    "TrustContext",
    "AuditLog",
    # Enums — exported so services/schemas can import from one place
    "UserStatus",
    "PolicyEffect",
    "RiskLevel",
    "AuditEventType",
    "AuditStatus",
]
