"""
DarkTrust – Trust Evaluator

Core service responsible for continuous evaluation of a request's SecurityContext.
Implements the 'Verify' step of Zero Trust.
"""

from app.security.security_context import SecurityContext
from app.security.exceptions import (
    ZeroTrustViolationException,
    UntrustedDeviceException,
    InsufficientTrustScoreException
)
from app.core.security import security_config

class TrustEvaluator:
    """
    Evaluates trust signals associated with a request context.
    Designed modularly so future engines (Risk, ML) can plug in.
    """
    
    @classmethod
    def evaluate_trust(cls, context: SecurityContext) -> bool:
        """
        Orchestrates all trust evaluation rules.
        Throws Zero Trust exceptions if any rule fails.
        Returns True if the context is fully trusted.
        """
        cls.check_user_status(context)
        cls.check_device_trust(context)
        cls.check_trust_score(context)
        # Future rules (IP Geolocation, Rate limiting anomalies) go here
        
        return True

    @classmethod
    def check_user_status(cls, context: SecurityContext) -> None:
        """
        Verifies the user account is fully active and not suspended.
        """
        if not context.user.is_active:
            raise ZeroTrustViolationException(detail="Account is currently inactive or suspended")

    @classmethod
    def check_device_trust(cls, context: SecurityContext) -> None:
        """
        Evaluates the device fingerprint.
        """
        # If the JWT token requires a device_id claim according to SecurityConfig
        # and the context doesn't have it, reject.
        if security_config.DEVICE_ID_CLAIM in security_config.REQUIRED_TOKEN_CLAIMS:
            if not context.device_id:
                raise UntrustedDeviceException(detail="Missing required device fingerprint")
                
        # Future implementation: Verify device_id against known/registered devices for the user

    @classmethod
    def check_trust_score(cls, context: SecurityContext) -> None:
        """
        Evaluates the contextual trust score against system baselines.
        """
        # Example threshold check (Threshold could be loaded dynamically based on requested resource)
        MINIMUM_TRUST_SCORE = 50.0
        
        if context.trust_score < MINIMUM_TRUST_SCORE:
            raise InsufficientTrustScoreException(
                detail=f"Trust score {context.trust_score} is below the required threshold of {MINIMUM_TRUST_SCORE}"
            )
