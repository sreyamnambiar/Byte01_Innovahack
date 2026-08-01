"""
DarkTrust – Authentication Module.

This module provides JWT-based authentication mechanisms, password hashing,
and FastAPI dependencies to secure endpoints.
"""

from app.auth.exceptions import (
    InvalidCredentialsException,
    InvalidTokenException,
    ExpiredTokenException,
    InactiveUserException,
)
from app.auth.password import get_password_hash, verify_password
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.auth.oauth2 import oauth2_scheme
from app.auth.dependencies import get_current_user, get_current_active_user

__all__ = [
    # Exceptions
    "InvalidCredentialsException",
    "InvalidTokenException",
    "ExpiredTokenException",
    "InactiveUserException",
    
    # Password
    "get_password_hash",
    "verify_password",
    
    # JWT
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    
    # OAuth2 & Dependencies
    "oauth2_scheme",
    "get_current_user",
    "get_current_active_user",
]
