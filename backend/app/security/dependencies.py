"""
DarkTrust – Zero Trust Dependencies

FastAPI dependency injectables that enforce the Zero Trust Policy Engine.
These integrate seamlessly with the existing JWT authentication layer.
"""

from fastapi import Depends, Request
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.auth.oauth2 import oauth2_scheme
from app.auth.jwt import decode_token
from app.core.security import security_config
from app.security.security_context import SecurityContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.security.policy_engine import PolicyEngine
from app.security.exceptions import ZeroTrustViolationException
from app.security.audit_logger import AuditLogger
from app.security.security_events import PolicyEvaluationEvent
from app.models.audit_log import AuditEventType, AuditStatus


async def get_security_context(
    request: Request,
    token: str = Depends(oauth2_scheme),
    user: User = Depends(get_current_user)
) -> SecurityContext:
    """
    Constructs the SecurityContext from the current HTTP request, 
    the decoded JWT token, and the authenticated User entity.
    """
    payload = decode_token(token)
    
    # Extract Trust signals from the token (if injected during login/refresh)
    # Defaulting to 100.0 for foundation testing
    trust_score = payload.get(security_config.TRUST_SCORE_CLAIM, 100.0)
    device_id = payload.get(security_config.DEVICE_ID_CLAIM)
    
    client_ip = request.client.host if request.client else None
    
    context = SecurityContext(
        user=user,
        token_payload=payload,
        client_ip=client_ip,
        device_id=device_id,
        trust_score=float(trust_score),
        metadata=dict(request.headers)
    )
    return context


def require_trust():
    """
    Dependency ensuring the request passes context evaluation (TrustEvaluator).
    Does NOT require specific RBAC permissions.
    """
    async def trust_checker(
        context: SecurityContext = Depends(get_security_context),
        session: AsyncSession = Depends(get_db)
    ) -> SecurityContext:
        try:
            PolicyEngine.evaluate_trust_only(context)
            
            await AuditLogger.log_policy_event(
                session,
                AuditEventType.ACCESS_GRANTED,
                PolicyEvaluationEvent(
                    user_id=context.user.id,
                    ip_address=context.client_ip,
                    user_agent=context.metadata.get("user-agent"),
                    action="trust_evaluation",
                    status=AuditStatus.SUCCESS
                )
            )
            return context
        except ZeroTrustViolationException as e:
            await AuditLogger.log_policy_event(
                session,
                AuditEventType.POLICY_VIOLATION,
                PolicyEvaluationEvent(
                    user_id=context.user.id,
                    ip_address=context.client_ip,
                    user_agent=context.metadata.get("user-agent"),
                    action="trust_evaluation",
                    status=AuditStatus.DENIED,
                    error_message=e.detail
                )
            )
            raise e
    return trust_checker


def require_policy(resource: str, action: str):
    """
    Dependency ensuring the request passes full Zero Trust evaluation.
    Evaluates Trust context AND enforces specific RBAC permissions.
    """
    async def policy_checker(
        context: SecurityContext = Depends(get_security_context),
        session: AsyncSession = Depends(get_db)
    ) -> SecurityContext:
        try:
            PolicyEngine.evaluate_policy(context, resource, action)
            
            await AuditLogger.log_policy_event(
                session,
                AuditEventType.ACCESS_GRANTED,
                PolicyEvaluationEvent(
                    user_id=context.user.id,
                    ip_address=context.client_ip,
                    user_agent=context.metadata.get("user-agent"),
                    resource=resource,
                    action=action,
                    status=AuditStatus.SUCCESS
                )
            )
            return context
        except ZeroTrustViolationException as e:
            await AuditLogger.log_policy_event(
                session,
                AuditEventType.POLICY_VIOLATION,
                PolicyEvaluationEvent(
                    user_id=context.user.id,
                    ip_address=context.client_ip,
                    user_agent=context.metadata.get("user-agent"),
                    resource=resource,
                    action=action,
                    status=AuditStatus.DENIED,
                    error_message=e.detail
                )
            )
            raise e
    return policy_checker
