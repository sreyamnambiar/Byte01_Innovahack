"""
DarkTrust – Zero Trust Security Platform
UserService

Orchestrates business logic for user management.
Delegates data persistence to the UserRepository.
"""

from uuid import UUID
from typing import Sequence

from app.models.user import User, UserStatus
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.services.exceptions import ResourceNotFoundException, ResourceAlreadyExistsException, ValidationException
from app.auth.password import get_password_hash


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def create_user(self, data: UserCreate) -> User:
        """
        Creates a new user.
        Validates uniqueness of email and username before insertion.
        NOTE: Password hashing is deferred to the Auth phase.
        """
        if await self.user_repo.email_exists(data.email):
            raise ResourceAlreadyExistsException(f"User with email {data.email} already exists.")
        
        if await self.user_repo.username_exists(data.username):
            raise ResourceAlreadyExistsException(f"User with username {data.username} already exists.")

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name,
            status=UserStatus.PENDING,
            is_active=True,
            is_superuser=False
        )

        return await self.user_repo.create(user)

    async def get_user(self, user_id: UUID) -> User:
        """
        Retrieves a user by ID. Raises ResourceNotFoundException if missing.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")
        return user

    async def update_user(self, user_id: UUID, data: dict) -> User:
        """
        Partially updates user details.
        """
        # Optionally, one could validate if they are changing email/username to avoid duplicates.
        if "email" in data and await self.user_repo.email_exists(data["email"]):
            existing_user = await self.user_repo.get_by_email(data["email"])
            if existing_user and existing_user.id != user_id:
                raise ResourceAlreadyExistsException(f"Email {data['email']} is already taken.")
                
        if "username" in data and await self.user_repo.username_exists(data["username"]):
            existing_user = await self.user_repo.get_by_username(data["username"])
            if existing_user and existing_user.id != user_id:
                raise ResourceAlreadyExistsException(f"Username {data['username']} is already taken.")

        updated_user = await self.user_repo.update_by_id(user_id, data)
        if not updated_user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")
        
        return updated_user

    async def delete_user(self, user_id: UUID) -> None:
        """
        Deletes a user by ID.
        """
        deleted = await self.user_repo.delete_by_id(user_id)
        if not deleted:
            raise ResourceNotFoundException(f"User with ID {user_id} not found.")
