"""
DarkTrust – Zero Trust Security Platform
Core Application Settings

Uses Pydantic Settings for type-safe, environment-driven configuration.
All settings are loaded from environment variables or the .env file.
"""

from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application-wide settings loaded from environment variables.

    Follows the 12-factor app methodology for configuration management.
    All values have sensible defaults for local development; production
    values MUST be provided via environment variables or secrets manager.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    APP_NAME: str = "DarkTrust"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Zero Trust Security Platform for Decentralized APIs"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------
    API_V1_PREFIX: str = "/api/v1"

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    DATABASE_URL: str = (
        "postgresql+asyncpg://darktrust_user:darktrust_pass@localhost:5432/darktrust_db"
    )
    DATABASE_SYNC_URL: str = (
        "postgresql://darktrust_user:darktrust_pass@localhost:5432/darktrust_db"
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30

    # ------------------------------------------------------------------
    # JWT Authentication
    # ------------------------------------------------------------------
    JWT_SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | List[str]) -> List[str]:
        """Parse comma-separated CORS origins from environment string."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------
    BCRYPT_ROUNDS: int = 12
    RATE_LIMIT_PER_MINUTE: int = 60

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------
    @property
    def is_production(self) -> bool:
        """True when running in production environment."""
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_debug(self) -> bool:
        """True when debug mode is enabled."""
        return self.DEBUG and not self.is_production


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached singleton instance of Settings.

    Using lru_cache ensures the .env file is read only once,
    and the same Settings object is reused across the application.
    Inject this via FastAPI's Depends() for testability.
    """
    return Settings()


# Module-level singleton for non-DI usage
settings: Settings = get_settings()
