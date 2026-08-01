"""
DarkTrust – Zero Trust Exceptions

Standardized FastAPI HTTP exceptions specifically tailored for the 
Zero Trust Policy Engine.
"""

from fastapi import HTTPException, status


class ZeroTrustViolationException(HTTPException):
    """Base exception for all Zero Trust policy rejections."""
    def __init__(self, detail: str = "Zero Trust Policy Violation: Access Denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class UntrustedDeviceException(ZeroTrustViolationException):
    """Raised when the request originates from an untrusted or anomalous device."""
    def __init__(self, detail: str = "Device trust verification failed"):
        super().__init__(detail=detail)


class InsufficientTrustScoreException(ZeroTrustViolationException):
    """Raised when the user's trust score drops below the required threshold."""
    def __init__(self, detail: str = "Insufficient trust score for requested action"):
        super().__init__(detail=detail)


class HighRiskException(ZeroTrustViolationException):
    """Raised when the Adaptive Risk Engine evaluates the request as HIGH RISK."""
    def __init__(self, detail: str = "Request denied due to high risk assessment"):
        super().__init__(detail=detail)


class RiskChallengeException(HTTPException):
    """Raised when the Risk Engine evaluates the request as MEDIUM RISK and requires a challenge (MFA)."""
    def __init__(self, detail: str = "Additional verification required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
