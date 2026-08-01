import os

try:
    from pydantic_settings import BaseSettings
except ImportError:
    class BaseSettings:
        pass

class Settings(BaseSettings):
    PROJECT_NAME: str = "DarkTrust Zero Trust Proxy"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "darktrust_zero_trust_super_secret_key_2026_innovahack")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Evaluation Metrics
    TARGET_PROXY_LATENCY_MS: float = 15.0  # <= 15ms overhead
    RISK_THRESHOLD_BLOCK: float = 75.0      # Block request if risk score > 75
    RISK_THRESHOLD_REAUTH: float = 50.0     # Require re-auth if risk score > 50

settings = Settings()
