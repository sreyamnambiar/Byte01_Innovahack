"""
DarkTrust – OAuth2 Integration

Configures FastAPI's OAuth2PasswordBearer to extract the token from the
Authorization header and ties it into OpenAPI/Swagger docs.
"""

from fastapi.security import OAuth2PasswordBearer

# The tokenUrl specifies the endpoint that clients will use to obtain a token.
# Note: The actual endpoint implementation is excluded from this phase.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scheme_name="JWT"
)
