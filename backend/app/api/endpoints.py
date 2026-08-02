import hashlib
import json
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, Header
from pydantic import BaseModel

from app.core.crypto import crypto_engine
from app.core.policy_engine import policy_engine
from app.core.proxy import service_mesh_proxy
from app.core.simulator import attack_simulator
from app.core.audit_logger import audit_logger

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    role: str = "guest"

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenRequest(BaseModel):
    caller_service: str
    target_service: str
    payload: Optional[Dict[str, Any]] = None

class ProxyEvalRequest(BaseModel):
    caller_service: str
    target_service: str
    token: str
    role: str = "user-service"
    client_ip: str = "10.0.1.1"
    geo: str = "US"
    payload_size_kb: float = 1.0
    payload: Optional[Dict[str, Any]] = None

class PolicyUpdateRequest(BaseModel):
    allowed_geos: Optional[List[str]] = None
    max_payload_kb: Optional[float] = None
    blocked_ips: Optional[List[str]] = None
    rbac_matrix: Optional[Dict[str, List[str]]] = None

class AttackSimRequest(BaseModel):
    scenario: str

@router.post("/auth/register")
def register_user(req: RegisterRequest):
    success, msg, user = crypto_engine.register_user(req.email, req.password, req.name, req.role)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "user": user}

@router.post("/auth/login")
def login_user(req: LoginRequest):
    success, msg, token, user = crypto_engine.authenticate_user(req.email, req.password)
    if not success:
        raise HTTPException(status_code=401, detail=msg)
    return {"message": msg, "access_token": token, "token_type": "bearer", "user": user}

@router.get("/auth/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    token = authorization.split(" ")[1]
    valid, reason, claims = crypto_engine.verify_service_token(token, "*")
    if not valid:
        raise HTTPException(status_code=401, detail=reason)
    return {"claims": claims, "status": "authenticated"}

@router.post("/auth/token")
def issue_service_token(req: TokenRequest):
    payload_hash = hashlib.sha256(json.dumps(req.payload or {}).encode()).hexdigest()[:16]
    token = crypto_engine.generate_service_token(req.target_service, req.caller_service, payload_hash)
    return {
        "token": token,
        "caller_service": req.caller_service,
        "target_service": req.target_service,
        "expires_in_seconds": 3600
    }

@router.post("/proxy/evaluate")
def evaluate_proxy_request(req: ProxyEvalRequest):
    context = {
        "role": req.role,
        "client_ip": req.client_ip,
        "geo": req.geo,
        "payload_size_kb": req.payload_size_kb,
        "action": "API_CALL"
    }
    is_allowed, reason, metrics = service_mesh_proxy.evaluate_request(
        caller_service=req.caller_service,
        target_service=req.target_service,
        token=req.token,
        context=context,
        payload=req.payload
    )
    return {
        "allowed": is_allowed,
        "reason": reason,
        "metrics": metrics
    }

@router.get("/policies")
def get_policies():
    return {
        "allowed_geos": policy_engine.allowed_geos,
        "blocked_ips": policy_engine.blocked_ips,
        "max_payload_kb": policy_engine.max_payload_kb,
        "time_restriction_enabled": policy_engine.time_restriction_enabled,
        "rbac_matrix": policy_engine.rbac_matrix
    }

@router.post("/policies")
def update_policies(req: PolicyUpdateRequest):
    policy_engine.update_policy(
        allowed_geos=req.allowed_geos,
        max_payload_kb=req.max_payload_kb,
        blocked_ips=req.blocked_ips,
        rbac_matrix=req.rbac_matrix
    )
    return {"status": "Policies updated successfully", "current_policies": get_policies()}

@router.get("/metrics")
def get_telemetry_metrics():
    return audit_logger.get_metrics()

@router.post("/attack-sim/run")
def trigger_attack_simulation(req: AttackSimRequest):
    result = attack_simulator.run_simulation(req.scenario)
    return result

@router.get("/logs")
def get_audit_logs(limit: int = Query(50, ge=1, le=200)):
    return {
        "logs": audit_logger.logs[:limit],
        "total_count": len(audit_logger.logs)
    }
