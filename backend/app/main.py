"""
DarkTrust – Zero Trust Security Platform
FastAPI Application Entry Point

This module creates and configures the FastAPI application instance.
It wires together:
  - CORS middleware
  - Logging initialization
  - API router registration
  - Swagger/OpenAPI configuration
  - Application lifespan (startup/shutdown hooks)
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.services.exceptions import (
    ResourceNotFoundException,
    ResourceAlreadyExistsException,
    ValidationException,
)
from app.security.exceptions import (
    ZeroTrustViolationException,
    HighRiskException,
    RiskChallengeException
)

# ---------------------------------------------------------------------------
# Module logger
# ---------------------------------------------------------------------------
log = get_logger(__name__)


# ---------------------------------------------------------------------------
# Application Lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI lifespan context manager for startup and shutdown events.

    Startup phase:
      - Initialize logging
      - Verify database connectivity (to be added with DB module)
      - Register background tasks (to be added with monitoring module)

    Shutdown phase:
      - Gracefully close database connections
      - Flush pending log records
    """
    # ── Startup ──────────────────────────────────────────────────────────
    setup_logging(
        log_level=settings.LOG_LEVEL,
        log_format=settings.LOG_FORMAT,
    )

    log.info(
        "Starting DarkTrust API",
        extra={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
        },
    )

    # TODO: Add database connectivity check here (future: DB module)
    # TODO: Add cache warm-up here (future: caching module)
    # TODO: Register background security tasks here (future: monitoring module)

    log.info("DarkTrust API startup complete — ready to serve requests")

    yield  # Application runs here

    # ── Shutdown ─────────────────────────────────────────────────────────
    log.info("Shutting down DarkTrust API")

    # TODO: Gracefully close DB engine here (future: DB module)
    # from app.database.engine import engine
    # await engine.dispose()

    log.info("DarkTrust API shutdown complete")


# ---------------------------------------------------------------------------
# FastAPI Application Factory
# ---------------------------------------------------------------------------
def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    Separating the factory function from module-level code enables:
    - Easier unit testing (create a fresh app per test)
    - Clean dependency injection
    - Configuration override in tests

    Returns:
        FastAPI: Fully configured application instance.
    """
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        lifespan=lifespan,
        # ── Swagger / OpenAPI ────────────────────────────────────────────
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        # ── OpenAPI Metadata ─────────────────────────────────────────────
        contact={
            "name": "DarkTrust Security Team",
            "url": "https://github.com/Byte01_Innovahack",
        },
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
        openapi_tags=[
            {
                "name": "System",
                "description": "Health checks, readiness probes, and system diagnostics.",
            },
            {
                "name": "Authentication",
                "description": "JWT authentication, token management. *(Future module)*",
            },
            {
                "name": "Policy Engine",
                "description": "Zero Trust policy definition and evaluation. *(Future module)*",
            },
            {
                "name": "API Gateway",
                "description": "Request routing, validation, and rate limiting. *(Future module)*",
            },
            {
                "name": "Audit Logs",
                "description": "Tamper-evident security event audit trail. *(Future module)*",
            },
        ],
    )

    # ── CORS Middleware ───────────────────────────────────────────────────
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # ── Custom Middleware (future modules register here) ──────────────────
    # from app.middleware.request_id import RequestIDMiddleware
    # from app.middleware.rate_limiter import RateLimitMiddleware
    # from app.middleware.trust_evaluator import TrustEvaluatorMiddleware
    # application.add_middleware(RequestIDMiddleware)
    # application.add_middleware(RateLimitMiddleware)
    # application.add_middleware(TrustEvaluatorMiddleware)

    # ── API Routers ───────────────────────────────────────────────────────
    application.include_router(v1_router)

    # ── Exception Handlers ────────────────────────────────────────────────
    @application.exception_handler(404)
    async def not_found_handler(request, exc) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "error": "not_found",
                "message": "The requested resource does not exist.",
                "path": str(request.url.path),
            },
        )

    @application.exception_handler(500)
    async def internal_error_handler(request, exc) -> JSONResponse:
        log.exception("Unhandled internal server error", extra={"path": str(request.url.path)})
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "message": "An unexpected error occurred. Please contact support.",
            },
        )

    @application.exception_handler(ResourceNotFoundException)
    async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @application.exception_handler(ResourceAlreadyExistsException)
    async def resource_exists_handler(request: Request, exc: ResourceAlreadyExistsException):
        return JSONResponse(status_code=409, content={"detail": exc.message})

    @application.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException):
        return JSONResponse(status_code=400, content={"detail": exc.message})

    @application.exception_handler(ZeroTrustViolationException)
    async def zero_trust_exception_handler(request: Request, exc: ZeroTrustViolationException):
        return JSONResponse(status_code=403, content={"detail": exc.detail})

    @application.exception_handler(HighRiskException)
    async def high_risk_exception_handler(request: Request, exc: HighRiskException):
        return JSONResponse(status_code=403, content={"detail": exc.detail})

    @application.exception_handler(RiskChallengeException)
    async def risk_challenge_exception_handler(request: Request, exc: RiskChallengeException):
        return JSONResponse(
            status_code=401, 
            content={"detail": exc.detail},
            headers=exc.headers
        )

    return application


# ---------------------------------------------------------------------------
# Application Instance
# ---------------------------------------------------------------------------
app: FastAPI = create_application()
