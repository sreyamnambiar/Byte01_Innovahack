"""
DarkTrust – Security Context

Defines the SecurityContext data structure representing the full 
evaluation state of a single API request for the Zero Trust Policy Engine.
"""

from typing import Any
from pydantic import BaseModel, Field
from app.models.user import User

class SecurityContext(BaseModel):
    """
    Encapsulates all contextual data surrounding an API request.
    Passed through the Trust Evaluator and Policy Engine.
    """
    # The authenticated user entity
    user: User
    
    # The raw JWT payload dictionary
    token_payload: dict[str, Any]
    
    # Client IP address making the request
    client_ip: str | None = None
    
    # Extracted device fingerprint from token or headers
    device_id: str | None = None
    
    # Pre-calculated trust score (to be expanded in the Risk Engine phase)
    trust_score: float = Field(default=100.0, description="Normalized score 0-100")
    
    # Additional request metadata (headers, user-agent, etc.)
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    model_config = {
        "arbitrary_types_allowed": True
    }
