"""
DarkTrust – Security module.

This module contains the Zero Trust Security Engine.
It evaluates contextual signals and orchestrates RBAC to ensure 
'Never Trust, Always Verify' is enforced on every request.
"""

from app.security.security_context import SecurityContext
from app.security.exceptions import (
    ZeroTrustViolationException,
    UntrustedDeviceException,
    InsufficientTrustScoreException,
    HighRiskException,
    RiskChallengeException
)
from app.security.trust_evaluator import TrustEvaluator
from app.security.policy_engine import PolicyEngine
from app.security.dependencies import (
    get_security_context,
    require_trust,
    require_policy
)
from app.security.risk_context import RiskContext, RiskResult, RiskLevel, RiskDecision
from app.security.risk_engine import RiskEngine

__all__ = [
    "SecurityContext",
    "ZeroTrustViolationException",
    "UntrustedDeviceException",
    "InsufficientTrustScoreException",
    "HighRiskException",
    "RiskChallengeException",
    "TrustEvaluator",
    "PolicyEngine",
    "get_security_context",
    "require_trust",
    "require_policy",
    "RiskContext",
    "RiskResult",
    "RiskLevel",
    "RiskDecision",
    "RiskEngine"
]
