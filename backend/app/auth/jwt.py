"""
DarkTrust – JWT Utilities

Handles creation, decoding, and validation of JSON Web Tokens.
Uses python-jose and integrates closely with SecurityConfig.
"""

from datetime import datetime, timezone
from typing import Any, Union
from uuid import UUID

from jose import jwt, JWTError, ExpiredSignatureError

from app.core.security import (
    security_config,
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
)
from app.auth.exceptions import InvalidTokenException, ExpiredTokenException


def create_access_token(subject: Union[str, UUID], extra_claims: dict[str, Any] | None = None) -> str:
    """
    Creates a short-lived access JWT.
    """
    now = datetime.now(timezone.utc)
    expire = now + security_config.access_token_expire

    to_encode = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
        "type": TOKEN_TYPE_ACCESS,
    }
    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(
        to_encode, 
        security_config.secret_key, 
        algorithm=security_config.algorithm
    )
    return encoded_jwt


def create_refresh_token(subject: Union[str, UUID], extra_claims: dict[str, Any] | None = None) -> str:
    """
    Creates a long-lived refresh JWT.
    """
    now = datetime.now(timezone.utc)
    expire = now + security_config.refresh_token_expire

    to_encode = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
        "type": TOKEN_TYPE_REFRESH,
    }
    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(
        to_encode, 
        security_config.secret_key, 
        algorithm=security_config.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """
    Decodes and validates a JWT token signature and expiration.
    Raises domain exceptions if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            security_config.secret_key,
            algorithms=[security_config.algorithm]
        )
        return payload
    except ExpiredSignatureError:
        raise ExpiredTokenException()
    except JWTError:
        raise InvalidTokenException()
