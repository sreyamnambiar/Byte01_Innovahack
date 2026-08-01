"""
DarkTrust – Authentication Tests
"""

import pytest
from app.auth.password import get_password_hash, verify_password
from app.auth.jwt import create_access_token, decode_token

@pytest.mark.asyncio
async def test_password_hashing():
    """Ensures passwords are securely hashed and verified."""
    password = "SuperSecretPassword123!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

@pytest.mark.asyncio
async def test_jwt_generation_and_decoding():
    """Ensures JWT tokens encode subjects correctly and can be decoded."""
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    token = create_access_token(subject=user_id)
    
    assert isinstance(token, str)
    
    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert "exp" in payload
