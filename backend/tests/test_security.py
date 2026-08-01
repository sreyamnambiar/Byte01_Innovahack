"""
DarkTrust – Security Engine Tests
"""

import pytest
from app.security.security_context import SecurityContext
from app.security.risk_context import RiskContext
from app.security.risk_engine import RiskEngine
from app.security.exceptions import HighRiskException
from app.security.attack_simulator.simulation_models import AttackType, AttackSeverity
from app.security.attack_simulator.attack_detector import AttackDetector

@pytest.mark.asyncio
async def test_attack_detector_sqli():
    """Ensures the AttackDetector successfully identifies SQLi signatures."""
    payload = {"username": "admin", "password": "' OR 1=1--"}
    is_detected, desc, severity = AttackDetector.analyze_payload(payload, AttackType.SQL_INJECTION)
    
    assert is_detected is True
    assert severity == AttackSeverity.CRITICAL

@pytest.mark.asyncio
async def test_risk_engine_velocity_block():
    """Ensures the RiskEngine throws HighRiskException on excessive failed logins."""
    mock_context = SecurityContext(
        user=None,
        token_payload={},
        client_ip="192.168.1.10",
        device_id="unknown",
        trust_score=100.0,
        metadata={}
    )
    
    # Simulate a brute force context (10 failed attempts)
    risk_context = RiskContext(security_context=mock_context, failed_login_attempts=10)
    
    risk_result = RiskEngine.evaluate_request_risk(risk_context)
    
    # We expect the score to skyrocket and the decision to be DENY
    assert risk_result.score >= 80.0
    assert risk_result.decision.value == "DENY"
    assert "VELOCITY_ANOMALY" in risk_result.triggered_factors
