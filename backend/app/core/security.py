"""
DarkTrust – Zero Trust Security Platform
JWT Security Configuration Stubs

This module contains ONLY the structural configuration for JWT security.
No authentication logic is implemented here.
Authentication endpoints, token generation, and validation logic
will be added to app/auth/ in future modules.
"""

from datetime import timedelta
from typing import Optional

from app.core.config import settings


# ------------------------------------------------------------------
# JWT Configuration Constants
# ------------------------------------------------------------------

ALGORITHM: str = settings.JWT_ALGORITHM
"""JWT signing algorithm (default: HS256)."""

ACCESS_TOKEN_EXPIRE: timedelta = timedelta(
    minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
)
"""Access token expiry duration."""

REFRESH_TOKEN_EXPIRE: timedelta = timedelta(
    days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
)
"""Refresh token expiry duration."""


# ------------------------------------------------------------------
# Token Type Constants
# ------------------------------------------------------------------

TOKEN_TYPE_ACCESS: str = "access"
TOKEN_TYPE_REFRESH: str = "refresh"


# ------------------------------------------------------------------
# Security Configuration
# ------------------------------------------------------------------

class SecurityConfig:
    """
    Centralized JWT and security configuration.

    This class exposes security-related constants derived from
    application settings. It acts as a single source of truth
    for all security parameters across the application.

    Authentication logic will be implemented in app/auth/ module.
    """

    secret_key: str = settings.JWT_SECRET_KEY
    algorithm: str = ALGORITHM
    access_token_expire: timedelta = ACCESS_TOKEN_EXPIRE
    refresh_token_expire: timedelta = REFRESH_TOKEN_EXPIRE
    bcrypt_rounds: int = settings.BCRYPT_ROUNDS

    # Placeholder for future Zero Trust token claims
    REQUIRED_TOKEN_CLAIMS: list[str] = ["sub", "iat", "exp", "type"]
    """Minimum required claims in every JWT token."""

    TRUST_SCORE_CLAIM: str = "trust_score"
    """Custom JWT claim key for Zero Trust risk/trust score."""

    DEVICE_ID_CLAIM: str = "device_id"
    """Custom JWT claim key for device fingerprint."""


# Module-level singleton
security_config = SecurityConfig()
