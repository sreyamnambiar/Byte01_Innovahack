"""
DarkTrust – Users API Router

Demonstrates RBAC-protected endpoints for user management.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.repositories.user_repository import UserRepository
from app.auth.dependencies import require_role, require_permission

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List all users (Admin only)",
    dependencies=[Depends(require_role("admin"))]
)
async def list_users(session: AsyncSession = Depends(get_db)):
    """
    Retrieves a list of all users. 
    Protected by RBAC: Requires 'admin' role.
    """
    user_repo = UserRepository(session)
    return await user_repo.get_all()


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    dependencies=[Depends(require_permission("user", "delete"))]
)
async def delete_user(user_id: str, session: AsyncSession = Depends(get_db)):
    """
    Deletes a specific user.
    Protected by RBAC: Requires 'delete' permission on 'user' resource.
    """
    # Note: Using str for user_id to avoid UUID parsing errors in URL for this sample
    import uuid
    user_uuid = uuid.UUID(user_id)
    
    user_repo = UserRepository(session)
    await user_repo.delete_by_id(user_uuid)
    return None
