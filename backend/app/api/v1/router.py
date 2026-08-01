"""
DarkTrust – Zero Trust Security Platform
API v1 Router

Aggregates all v1 endpoint routers into a single versioned router.
Future modules (auth, policies, gateway, audit) register sub-routers here.
"""

from fastapi import APIRouter

# ---------------------------------------------------------------------------
# v1 Root Router
# ---------------------------------------------------------------------------
router = APIRouter(prefix="/api/v1")


# ---------------------------------------------------------------------------
# Health Check Endpoint
# ---------------------------------------------------------------------------
@router.get(
    "/health",
    tags=["System"],
    summary="Health Check",
    description=(
        "Returns the current health status of the DarkTrust API. "
        "Used by load balancers, orchestrators, and monitoring systems."
    ),
    response_description="Service health status",
)
async def health_check() -> dict:
    """
    Lightweight health check endpoint.

    Returns a 200 OK with service status when the API is running.
    Does NOT check database connectivity (use /readiness for that).
    """
    return {
        "status": "healthy",
        "service": "DarkTrust API",
        "version": "1.0.0",
    }


@router.get(
    "/readiness",
    tags=["System"],
    summary="Readiness Check",
    description=(
        "Checks whether the service is ready to handle requests. "
        "Verifies database connectivity and critical dependencies."
    ),
    response_description="Service readiness status",
)
async def readiness_check() -> dict:
    """
    Readiness probe endpoint.

    Future implementation will verify:
    - Database connectivity
    - Cache availability
    - External service dependencies

    Returns 200 when all dependencies are reachable.
    """
    # TODO: Add actual dependency health checks in future modules
    return {
        "status": "ready",
        "dependencies": {
            "database": "not_checked",  # Will be implemented with DB module
        },
    }


# ---------------------------------------------------------------------------
# Future Module Router Registration
# ---------------------------------------------------------------------------
# Uncomment and import as each module is developed:
#
# from app.api.v1.endpoints import auth, users, policies, gateway, audit
# router.include_router(auth.router,     prefix="/auth",     tags=["Authentication"])
# router.include_router(users.router,    prefix="/users",    tags=["Users"])
# router.include_router(policies.router, prefix="/policies", tags=["Policy Engine"])
# router.include_router(gateway.router,  prefix="/gateway",  tags=["API Gateway"])
# router.include_router(audit.router,    prefix="/audit",    tags=["Audit Logs"])
