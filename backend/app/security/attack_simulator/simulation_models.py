"""
DarkTrust – Attack Simulation Models

Defines the Pydantic schemas for the educational Attack Simulator.
"""

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class AttackSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AttackType(str, Enum):
    BRUTE_FORCE = "brute_force"
    TOKEN_REPLAY = "token_replay"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    PATH_TRAVERSAL = "path_traversal"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    API_ENUMERATION = "api_enumeration"

class SimulationRequest(BaseModel):
    """Payload submitted to trigger a specific attack simulation."""
    attack_type: AttackType
    target_endpoint: str = "/api/v1/protected-resource"
    payload: dict[str, Any] | None = None
    headers: dict[str, str] | None = None
    client_ip: str = "192.168.1.100"

class SimulationResult(BaseModel):
    """The detailed report generated after a simulated attack is intercepted."""
    attack_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    attack_type: AttackType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: uuid.UUID | None = None
    client_ip: str
    target_endpoint: str
    risk_score: float
    trust_score: float
    detection_status: str
    security_decision: str
    recommended_action: str
