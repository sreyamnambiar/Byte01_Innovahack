"""
DarkTrust – Authentication Dependencies

FastAPI dependency injectables used in route handlers to enforce authentication.
Extracts token from request, validates it, and fetches the User model.
"""

from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.oauth2 import oauth2_scheme
from app.auth.jwt import decode_token
from app.auth.exceptions import InvalidTokenException, InactiveUserException
from app.models.user import User
from app.database.session import get_db
from app.repositories.user_repository import UserRepository


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> User:
    """
    Validates the Bearer token, extracts the subject (user_id), and
    retrieves the User from the database.
    """
    payload = decode_token(token)
    
    # We expect 'sub' to be the user_id (UUID)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise InvalidTokenException(detail="Token payload missing subject claim")
        
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise InvalidTokenException(detail="Token subject is not a valid UUID")

    # Fetch user using UserRepository
    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise InvalidTokenException(detail="User not found")
        
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Ensures that the authenticated user is currently active.
    This should be used on almost all endpoints protecting active resources.
    """
    if not current_user.is_active:
        raise InactiveUserException()
    return current_user
