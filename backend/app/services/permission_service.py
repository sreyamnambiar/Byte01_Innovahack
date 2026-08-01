"""
DarkTrust – Zero Trust Security Platform
PermissionService

Orchestrates business logic for permission management and role delegation.
Delegates data persistence to the PermissionRepository and RoleRepository.
"""

from uuid import UUID
from typing import Sequence

from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.permission import PermissionCreate
from app.services.exceptions import ResourceNotFoundException, ResourceAlreadyExistsException, ValidationException
from sqlalchemy.exc import IntegrityError


class PermissionService:
    def __init__(self, permission_repo: PermissionRepository, role_repo: RoleRepository) -> None:
        self.permission_repo = permission_repo
        self.role_repo = role_repo

    async def create_permission(self, data: PermissionCreate) -> Permission:
        """
        Creates a new permission.
        Validates uniqueness of the resource/action combination.
        """
        if await self.permission_repo.name_exists(data.name):
            raise ResourceAlreadyExistsException(f"Permission with name '{data.name}' already exists.")
            
        if await self.permission_repo.resource_action_exists(data.resource, data.action):
            raise ResourceAlreadyExistsException(f"Permission for resource '{data.resource}' and action '{data.action}' already exists.")

        permission = Permission(
            name=data.name,
            resource=data.resource,
            action=data.action,
            description=data.description
        )

        return await self.permission_repo.create(permission)

    async def assign_permission_to_role(self, role_id: UUID, permission_id: UUID) -> RolePermission:
        """
        Assigns a permission to a role.
        """
        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise ResourceNotFoundException(f"Role with ID {role_id} not found.")

        permission = await self.permission_repo.get_by_id(permission_id)
        if not permission:
            raise ResourceNotFoundException(f"Permission with ID {permission_id} not found.")

        try:
            return await self.role_repo.assign_permission(role_id=role_id, permission_id=permission_id)
        except IntegrityError:
            raise ResourceAlreadyExistsException("Permission is already assigned to this role.")

    async def remove_permission_from_role(self, role_id: UUID, permission_id: UUID) -> None:
        """
        Removes a permission assignment from a role.
        """
        removed = await self.role_repo.revoke_permission(role_id, permission_id)
        if not removed:
            raise ResourceNotFoundException("Permission assignment does not exist for this role.")

    async def list_role_permissions(self, role_id: UUID) -> Sequence[Permission]:
        """
        Retrieves all permissions assigned to a role.
        """
        role = await self.role_repo.get_with_permissions(role_id)
        if not role:
            raise ResourceNotFoundException(f"Role with ID {role_id} not found.")
            
        return [rp.permission for rp in role.role_permissions]
