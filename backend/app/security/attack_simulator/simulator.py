"""
DarkTrust – Simulator Orchestrator

Executes the simulated attack by forging a SecurityContext and passing it 
through the real Zero Trust Policy Engine and Risk Engine.
"""

from typing import Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.security.security_context import SecurityContext
from app.security.risk_context import RiskContext, RiskDecision
from app.security.policy_engine import PolicyEngine
from app.security.risk_engine import RiskEngine
from app.security.exceptions import ZeroTrustViolationException, HighRiskException, RiskChallengeException
from app.security.attack_simulator.simulation_models import SimulationRequest, SimulationResult, AttackSeverity
from app.security.attack_simulator.attack_detector import AttackDetector
from app.security.audit_logger import AuditLogger
from app.security.security_events import PolicyEvaluationEvent
from app.models.audit_log import AuditEventType, AuditStatus

class AttackSimulator:

    @classmethod
    async def simulate_attack(
        cls, 
        session: AsyncSession, 
        user: User, 
        request: SimulationRequest
    ) -> SimulationResult:
        """
        Orchestrates the attack simulation through DarkTrust's actual defenses.
        """
        # 1. Detect Payload Severity
        is_detected, description, severity = AttackDetector.analyze_payload(request.payload, request.attack_type)
        
        # 2. Forge a Security Context representing the attacker
        # We manually lower the trust score if the severity is high to trigger Risk Engine
        mock_trust_score = 100.0 if severity == AttackSeverity.LOW else 40.0
        
        context = SecurityContext(
            user=user,
            token_payload={},
            client_ip=request.client_ip,
            device_id="unregistered-simulator-device" if request.attack_type.value in ["token_replay", "brute_force"] else "sim-device",
            trust_score=mock_trust_score,
            metadata=request.headers or {}
        )
        
        risk_context = RiskContext(
            security_context=context,
            failed_login_attempts=5 if request.attack_type.value == "brute_force" else 0
        )
        
        detection_status = "Bypassed"
        security_decision = "ALLOWED"
        recommended_action = "None"
        final_risk_score = 0.0

        try:
            # 3. Fire it through the Risk Engine directly (or Policy Engine)
            # Since this is an attack, we'll run Risk Engine directly to get the score
            risk_result = RiskEngine.evaluate_request_risk(risk_context)
            final_risk_score = risk_result.score
            
            if risk_result.decision == RiskDecision.DENY:
                raise HighRiskException(detail=f"Blocked by Risk Engine. Factors: {', '.join(risk_result.triggered_factors)}")
                
            # If Risk allows, try Policy Engine (Trust Evaluator)
            PolicyEngine.evaluate_trust_only(context)
            
        except HighRiskException as e:
            detection_status = "Intercepted by Risk Engine"
            security_decision = "DENIED (HIGH RISK)"
            recommended_action = "Block IP and invalidate active sessions."
        except ZeroTrustViolationException as e:
            detection_status = "Intercepted by Trust Evaluator"
            security_decision = "DENIED (ZERO TRUST VIOLATION)"
            recommended_action = "Require MFA verification."
            
        # 4. Audit Log the simulated attack
        await AuditLogger.log_policy_event(
            session,
            AuditEventType.ATTACK_DETECTED,
            PolicyEvaluationEvent(
                user_id=user.id,
                ip_address=request.client_ip,
                user_agent=context.metadata.get("user-agent", "simulator"),
                action=request.attack_type.value,
                resource=request.target_endpoint,
                status=AuditStatus.DENIED if "DENIED" in security_decision else AuditStatus.SUCCESS,
                error_message=detection_status,
                extra_metadata={"severity": severity.value, "description": description}
            )
        )

        return SimulationResult(
            attack_type=request.attack_type,
            user_id=user.id,
            client_ip=request.client_ip,
            target_endpoint=request.target_endpoint,
            risk_score=final_risk_score,
            trust_score=context.trust_score,
            detection_status=detection_status,
            security_decision=security_decision,
            recommended_action=recommended_action
        )
