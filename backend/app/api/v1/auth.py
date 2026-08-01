"""
DarkTrust – Authentication API Router

Exposes public REST API endpoints for user registration, login, token refresh,
and authenticated identity retrieval.
"""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, RefreshTokenRequest
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.auth.password import verify_password
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.auth.exceptions import InvalidCredentialsException, InvalidTokenException
from app.auth.dependencies import get_current_user, get_current_active_user
from app.core.security import TOKEN_TYPE_REFRESH
from app.security.audit_logger import AuditLogger
from app.security.security_events import AuthenticationEvent
from app.models.audit_log import AuditEventType, AuditStatus

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(session))


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register(
    data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db)
):
    """
    Registers a new DarkTrust user account.
    Returns the user representation without the password.
    """
    user = await user_service.create_user(data)
    
    await AuditLogger.log_authentication_event(
        session,
        AuditEventType.USER_CREATED,
        AuthenticationEvent(
            user_id=user.id,
            action="register",
            resource="user",
            resource_id=str(user.id),
        )
    )
    
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Login via OAuth2 password flow"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    """
    Authenticates a user via username and password.
    Returns a JWT access token and a refresh token.
    """
    user_repo = UserRepository(session)
    user = await user_repo.get_by_username(form_data.username)
    
    # If username not found, try email (optional convenience)
    if not user:
        user = await user_repo.get_by_email(form_data.username)

    if not user:
        await AuditLogger.log_authentication_event(
            session,
            AuditEventType.LOGIN_FAILURE,
            AuthenticationEvent(
                action="login",
                metadata={"username": form_data.username}
            )
        )
        raise InvalidCredentialsException()

    if not verify_password(form_data.password, user.hashed_password):
        await AuditLogger.log_authentication_event(
            session,
            AuditEventType.LOGIN_FAILURE,
            AuthenticationEvent(
                user_id=user.id,
                action="login"
            )
        )
        raise InvalidCredentialsException()

    # Create tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    await AuditLogger.log_authentication_event(
        session,
        AuditEventType.LOGIN_SUCCESS,
        AuthenticationEvent(
            user_id=user.id,
            action="login"
        )
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh an expired access token"
)
async def refresh_token(
    data: RefreshTokenRequest,
    session: AsyncSession = Depends(get_db)
):
    """
    Accepts a valid refresh token and returns a new access token and refresh token.
    """
    payload = decode_token(data.refresh_token)
    
    if payload.get("type") != TOKEN_TYPE_REFRESH:
        raise InvalidTokenException(detail="Provided token is not a refresh token")
        
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise InvalidTokenException(detail="Token payload missing subject claim")

    # Issue new tokens
    access_token = create_access_token(subject=user_id_str)
    new_refresh_token = create_refresh_token(subject=user_id_str)

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout current user"
)
async def logout(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    """
    Logs out the user. 
    (Note: JWTs are stateless. Token revocation/blacklisting will be implemented here later).
    """
    await AuditLogger.log_authentication_event(
        session,
        AuditEventType.LOGOUT,
        AuthenticationEvent(
            user_id=current_user.id,
            action="logout"
        )
    )
    return {"message": "Successfully logged out"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current active user"
)
async def get_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Returns the profile of the currently authenticated and active user.
    """
    return current_user
