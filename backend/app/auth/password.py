"""
DarkTrust – Password Security

Handles secure password hashing and verification using passlib and bcrypt.
Configured via the centralized SecurityConfig.
"""

from passlib.context import CryptContext
from app.core.security import security_config

# CryptContext configured to use bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=security_config.bcrypt_rounds
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against its hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.
    """
    return pwd_context.hash(password)
