"""
DarkTrust – RBAC Utilities

Helper functions to inspect a user's roles and permissions.
Assumes the User model has loaded `user_roles` and `role_permissions`
relationships via SQLAlchemy (e.g., lazy="selectin").
"""

from typing import Sequence
from app.models.user import User

def get_user_roles(user: User) -> list[str]:
    """
    Returns a list of active role names assigned to the user.
    """
    active_roles = []
    for user_role in user.user_roles:
        role = user_role.role
        if role and role.is_active:
            active_roles.append(role.name.lower())
    return active_roles

def get_user_permissions(user: User) -> list[dict[str, str]]:
    """
    Returns a list of dictionaries representing active permissions 
    assigned to the user via their active roles.
    Format: [{"resource": "user", "action": "create"}, ...]
    """
    permissions = []
    for user_role in user.user_roles:
        role = user_role.role
        if role and role.is_active:
            for role_perm in role.role_permissions:
                perm = role_perm.permission
                if perm:
                    permissions.append({
                        "resource": perm.resource.lower(),
                        "action": perm.action.lower()
                    })
    return permissions

def has_role(user: User, role_name: str) -> bool:
    """
    Checks if the user has a specific role.
    """
    if user.is_superuser:
        return True
    return role_name.lower() in get_user_roles(user)

def has_permission(user: User, resource: str, action: str) -> bool:
    """
    Checks if the user has a specific permission via their roles.
    """
    if user.is_superuser:
        return True
    
    res = resource.lower()
    act = action.lower()
    
    for perm in get_user_permissions(user):
        if perm["resource"] == res and perm["action"] == act:
            return True
        # Support for wildcard actions if needed in the future
        if perm["resource"] == res and perm["action"] == "*":
            return True
            
    return False
