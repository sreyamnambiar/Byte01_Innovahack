"""
DarkTrust – Risk Engine

Orchestrates the evaluation of risk rules against a context, calculates 
a final dynamic score, and issues a decision (ALLOW, CHALLENGE, DENY).
"""

from app.security.risk_context import RiskContext, RiskResult, RiskLevel, RiskDecision
from app.security.risk_rules import ACTIVE_RISK_RULES

class RiskEngine:
    
    @classmethod
    def evaluate_request_risk(cls, context: RiskContext) -> RiskResult:
        """
        Primary entry point. Orchestrates the calculation and classification.
        """
        score, factors = cls.calculate_risk_score(context)
        level = cls.classify_risk(score)
        decision = cls.generate_decision(level)
        
        return RiskResult(
            score=score,
            level=level,
            decision=decision,
            triggered_factors=factors
        )

    @classmethod
    def calculate_risk_score(cls, context: RiskContext) -> tuple[int, list[str]]:
        """
        Iterates over all ACTIVE_RISK_RULES, summing penalties.
        Base score is 0. Maximum score is 100.
        """
        total_penalty = 0
        triggered_factors = []
        
        for rule in ACTIVE_RISK_RULES:
            penalty, factor_desc = rule(context)
            if penalty > 0 and factor_desc:
                total_penalty += penalty
                triggered_factors.append(factor_desc)
                
        # Ensure score stays within 0-100 bounds
        final_score = min(max(total_penalty, 0), 100)
        return final_score, triggered_factors

    @classmethod
    def classify_risk(cls, score: int) -> RiskLevel:
        """
        Categorizes the numeric score into a RiskLevel.
        0-30 -> LOW
        31-60 -> MEDIUM
        61-100 -> HIGH
        """
        if score <= 30:
            return RiskLevel.LOW
        elif score <= 60:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH

    @classmethod
    def generate_decision(cls, level: RiskLevel) -> RiskDecision:
        """
        Maps a RiskLevel to an actionable RiskDecision.
        """
        if level == RiskLevel.LOW:
            return RiskDecision.ALLOW
        elif level == RiskLevel.MEDIUM:
            return RiskDecision.CHALLENGE
        else:
            return RiskDecision.DENY
