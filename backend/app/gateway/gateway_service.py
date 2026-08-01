"""
DarkTrust – Gateway Service

Business logic for the gateway operations, focusing on health checks,
readiness probes, and status telemetry.
"""

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class GatewayService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def check_database_readiness(self) -> bool:
        """
        Executes a lightweight query to verify the database connection is alive.
        """
        try:
            await self.session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    async def get_gateway_status(self) -> dict[str, Any]:
        """
        Returns operational metrics of the API Gateway.
        """
        db_ready = await self.check_database_readiness()
        
        return {
            "status": "operational" if db_ready else "degraded",
            "modules": {
                "authentication": "online",
                "rbac_engine": "online",
                "zero_trust_policy": "online",
                "risk_engine": "online",
                "audit_logger": "online",
                "database": "connected" if db_ready else "disconnected"
            },
            "security_perimeter": "active"
        }
