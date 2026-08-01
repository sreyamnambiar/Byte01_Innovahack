"""
DarkTrust – Token Pydantic Schemas

Schemas for representing authentication tokens in HTTP responses.
"""

from pydantic import BaseModel, Field

class Token(BaseModel):
    """
    Standard OAuth2 / JWT token response schema.
    Returned upon successful authentication.
    """
    access_token: str = Field(..., description="Short-lived access JWT")
    refresh_token: str = Field(..., description="Long-lived refresh JWT")
    token_type: str = Field(default="bearer", description="Token type, always 'bearer'")

class RefreshTokenRequest(BaseModel):
    """
    Schema for requesting a new access token using a refresh token.
    """
    refresh_token: str = Field(..., description="Valid refresh JWT")
