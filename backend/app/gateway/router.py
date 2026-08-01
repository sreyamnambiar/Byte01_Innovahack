"""
DarkTrust – API Gateway Router

Exposes structural health and readiness endpoints.
These are often consumed by load balancers, orchestrators, and monitoring agents.
"""

from typing import Any
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.gateway.gateway_service import GatewayService
from app.auth.dependencies import require_role

router = APIRouter(tags=["API Gateway"])

def get_gateway_service(session: AsyncSession = Depends(get_db)) -> GatewayService:
    return GatewayService(session)

@router.get("/health", status_code=status.HTTP_200_OK, summary="Liveness Probe")
async def health_check():
    """
    Returns 200 OK if the FastAPI server is running.
    """
    return {"status": "ok"}


@router.get("/readiness", summary="Readiness Probe")
async def readiness_check(gateway_service: GatewayService = Depends(get_gateway_service)):
    """
    Verifies critical backing services (e.g., PostgreSQL) are online.
    """
    is_ready = await gateway_service.check_database_readiness()
    if not is_ready:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database is unreachable")
    return {"status": "ready"}


@router.get(
    "/gateway/status", 
    summary="Gateway Operational Status",
    dependencies=[Depends(require_role("admin"))]
)
async def gateway_status(gateway_service: GatewayService = Depends(get_gateway_service)) -> dict[str, Any]:
    """
    Provides an overarching view of the security platform's health.
    Locked behind admin RBAC.
    """
    return await gateway_service.get_gateway_status()
