"""
DarkTrust – Audit Logger

Utility class dedicated to the construction and database insertion of 
AuditLog records. Decouples the ORM models from the rest of the application.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog, AuditEventType
from app.security.security_events import AuthenticationEvent, AuthorizationEvent, PolicyEvaluationEvent

class AuditLogger:
    
    @staticmethod
    async def _insert_log(session: AsyncSession, log_entry: AuditLog) -> None:
        """Internal helper to insert the log."""
        session.add(log_entry)
        await session.commit()
        await session.refresh(log_entry)

    @classmethod
    async def log_authentication_event(
        cls, 
        session: AsyncSession, 
        event_type: AuditEventType, 
        payload: AuthenticationEvent
    ) -> None:
        """Logs login, logout, and registration events."""
        log = AuditLog(
            event_type=event_type,
            user_id=payload.user_id,
            ip_address=payload.ip_address,
            user_agent=payload.user_agent,
            resource=payload.resource,
            resource_id=payload.resource_id,
            action=payload.action,
            status=payload.status,
            error_message=payload.error_message,
            extra_metadata=payload.extra_metadata
        )
        await cls._insert_log(session, log)

    @classmethod
    async def log_authorization_event(
        cls, 
        session: AsyncSession, 
        event_type: AuditEventType, 
        payload: AuthorizationEvent
    ) -> None:
        """Logs role and permission changes."""
        log = AuditLog(
            event_type=event_type,
            user_id=payload.user_id,
            ip_address=payload.ip_address,
            user_agent=payload.user_agent,
            resource=payload.resource,
            resource_id=payload.resource_id,
            action=payload.action,
            status=payload.status,
            error_message=payload.error_message,
            old_values=payload.old_values,
            new_values=payload.new_values,
            extra_metadata=payload.extra_metadata
        )
        await cls._insert_log(session, log)

    @classmethod
    async def log_policy_event(
        cls, 
        session: AsyncSession, 
        event_type: AuditEventType, 
        payload: PolicyEvaluationEvent
    ) -> None:
        """Logs Zero Trust Policy Engine decisions (Allow/Deny)."""
        log = AuditLog(
            event_type=event_type,
            user_id=payload.user_id,
            request_id=payload.request_id,
            trust_context_id=payload.trust_context_id,
            ip_address=payload.ip_address,
            user_agent=payload.user_agent,
            resource=payload.resource,
            resource_id=payload.resource_id,
            action=payload.action,
            status=payload.status,
            error_message=payload.error_message,
            extra_metadata=payload.extra_metadata
        )
        await cls._insert_log(session, log)
