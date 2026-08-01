"""
DarkTrust – Zero Trust Security Platform
RoleService

Orchestrates business logic for role management and assignment.
Delegates data persistence to the RoleRepository and UserRepository.
"""

from uuid import UUID
from typing import Sequence

from app.models.role import Role
from app.models.user_role import UserRole
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.schemas.role import RoleCreate
from app.services.exceptions import ResourceNotFoundException, ResourceAlreadyExistsException, ValidationException
from sqlalchemy.exc import IntegrityError
from app.security.audit_logger import AuditLogger
from app.security.security_events import AuthorizationEvent
from app.models.audit_log import AuditEventType


class RoleService:
    def __init__(self, role_repo: RoleRepository, user_repo: UserRepository) -> None:
        self.role_repo = role_repo
        self.user_repo = user_repo

    async def create_role(self, data: RoleCreate) -> Role:
        """
        Creates a new role.
        Validates uniqueness of role name.
        """
        if await self.role_repo.name_exists(data.name):
            raise ResourceAlreadyExistsException(f"Role with name '{data.name}' already exists.")

        role = Role(
            name=data.name.lower().strip(),
            description=data.description,
            is_active=True
        )

        return await self.role_repo.create(role)

    async def assign_role_to_user(self, user_id: UUID, role_id: UUID, assigned_by: UUID | None = None) -> UserRole:
        """
        Assigns a role to a user.
        Ensures both user and role exist and are active.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")
        if not user.is_active:
            raise ValidationException("Cannot assign roles to an inactive user.")

        role = await self.role_repo.get_by_id(role_id)
        if not role:
            raise ResourceNotFoundException(f"Role with ID {role_id} not found.")
        if not role.is_active:
            raise ValidationException("Cannot assign an inactive role.")

        try:
            assignment = await self.role_repo.assign_to_user(user_id=user_id, role_id=role_id, assigned_by=assigned_by)
            await AuditLogger.log_authorization_event(
                self.role_repo.session,
                AuditEventType.ROLE_ASSIGNED,
                AuthorizationEvent(
                    user_id=assigned_by,
                    action="assign_role",
                    resource="user_role",
                    resource_id=str(user_id),
                    new_values={"role_id": str(role_id), "user_id": str(user_id)}
                )
            )
            return assignment
        except IntegrityError:
            raise ResourceAlreadyExistsException("Role is already assigned to this user.")

    async def remove_role_from_user(self, user_id: UUID, role_id: UUID) -> None:
        """
        Removes a role assignment from a user.
        """
        removed = await self.role_repo.revoke_from_user(user_id, role_id)
        if not removed:
            raise ResourceNotFoundException("Role assignment does not exist for this user.")
            
        await AuditLogger.log_authorization_event(
            self.role_repo.session,
            AuditEventType.ROLE_REVOKED,
            AuthorizationEvent(
                user_id=None,  # We don't have assigned_by here, could be passed
                action="revoke_role",
                resource="user_role",
                resource_id=str(user_id),
                old_values={"role_id": str(role_id), "user_id": str(user_id)}
            )
        )

    async def list_user_roles(self, user_id: UUID) -> Sequence[Role]:
        """
        Retrieves all roles assigned to a user.
        """
        user = await self.user_repo.get_with_roles(user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")
            
        return [user_role.role for user_role in user.user_roles]
