"""
DarkTrust – Policy Engine

Orchestrates the entire authorization flow, seamlessly tying RBAC and the 
Trust Evaluator together to form the complete Zero Trust evaluation pipeline.
"""

from app.security.security_context import SecurityContext
from app.security.trust_evaluator import TrustEvaluator
from app.auth.rbac import has_permission
from app.security.exceptions import ZeroTrustViolationException, HighRiskException, RiskChallengeException
from app.security.risk_context import RiskContext, RiskDecision
from app.security.risk_engine import RiskEngine

class PolicyEngine:
    """
    Central engine for determining if a request is authorized.
    Evaluates Trust (Context) first, then applies RBAC (Permissions).
    """

    @classmethod
    def evaluate_policy(cls, context: SecurityContext, resource: str, action: str) -> bool:
        """
        Executes the end-to-end Zero Trust pipeline.
        
        1. Contextual Trust Evaluation (Never Trust, Always Verify)
        2. Static Role-Based Access Control (Permissions)
        
        Raises ZeroTrustViolationException if rejected.
        """
        # 1. Evaluate Trust Context (Baseline Signals)
        TrustEvaluator.evaluate_trust(context)
        
        # 2. Evaluate RBAC Permissions (Static Authorization)
        if not has_permission(context.user, resource, action):
            raise ZeroTrustViolationException(
                detail=f"Policy Denied: User lacks permission '{action}' on resource '{resource}'"
            )
            
        # 3. Evaluate Dynamic Risk (Adaptive Risk Engine)
        # Construct RiskContext (stubbing failed logins for now)
        risk_context = RiskContext(security_context=context, failed_login_attempts=0)
        risk_result = RiskEngine.evaluate_request_risk(risk_context)
        
        if risk_result.decision == RiskDecision.DENY:
            factors = ", ".join(risk_result.triggered_factors)
            raise HighRiskException(detail=f"Request denied due to HIGH risk. Factors: {factors}")
        elif risk_result.decision == RiskDecision.CHALLENGE:
            raise RiskChallengeException(detail="Medium risk detected. Additional verification (MFA) required.")
            
        return True
        
    @classmethod
    def evaluate_trust_only(cls, context: SecurityContext) -> bool:
        """
        Evaluates the Trust Context without requiring specific RBAC permissions.
        Useful for generic endpoints that are available to any trusted active user.
        """
        return TrustEvaluator.evaluate_trust(context)
