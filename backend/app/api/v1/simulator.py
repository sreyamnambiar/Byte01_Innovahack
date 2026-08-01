"""
DarkTrust – Attack Simulator API

Educational endpoints designed exclusively for the hackathon to demonstrate 
the platform's active defense capabilities.
These endpoints are locked to administrators only.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.user import User
from app.auth.dependencies import require_role, get_current_active_user
from app.security.attack_simulator.simulation_models import SimulationRequest, SimulationResult, AttackType
from app.security.attack_simulator.simulation_service import SimulationService

router = APIRouter(
    prefix="/simulator",
    tags=["Attack Simulator (Educational)"],
    dependencies=[Depends(require_role("admin"))]
)

def get_simulation_service(session: AsyncSession = Depends(get_db)) -> SimulationService:
    return SimulationService(session)

@router.post(
    "/sql-injection",
    response_model=SimulationResult,
    summary="Simulate SQL Injection Attack",
    description="Submits a standard SQLi payload to demonstrate interception by the detection engine."
)
async def simulate_sqli(
    request: SimulationRequest,
    current_user: User = Depends(get_current_active_user),
    service: SimulationService = Depends(get_simulation_service)
):
    request.attack_type = AttackType.SQL_INJECTION
    return await service.run_simulation(current_user, request)

@router.post(
    "/xss",
    response_model=SimulationResult,
    summary="Simulate Cross-Site Scripting (XSS)",
    description="Submits a Cross-Site Scripting payload to demonstrate the firewall rules."
)
async def simulate_xss(
    request: SimulationRequest,
    current_user: User = Depends(get_current_active_user),
    service: SimulationService = Depends(get_simulation_service)
):
    request.attack_type = AttackType.XSS
    return await service.run_simulation(current_user, request)

@router.post(
    "/token-replay",
    response_model=SimulationResult,
    summary="Simulate Token Replay",
    description="Attempts to reuse a simulated hijacked token to demonstrate the Zero Trust device identity rules."
)
async def simulate_token_replay(
    request: SimulationRequest,
    current_user: User = Depends(get_current_active_user),
    service: SimulationService = Depends(get_simulation_service)
):
    request.attack_type = AttackType.TOKEN_REPLAY
    return await service.run_simulation(current_user, request)

@router.post(
    "/bruteforce",
    response_model=SimulationResult,
    summary="Simulate Brute Force Login",
    description="Simulates excessive login failures to trigger the Risk Engine velocity blockers."
)
async def simulate_bruteforce(
    request: SimulationRequest,
    current_user: User = Depends(get_current_active_user),
    service: SimulationService = Depends(get_simulation_service)
):
    request.attack_type = AttackType.BRUTE_FORCE
    return await service.run_simulation(current_user, request)

@router.post(
    "/path-traversal",
    response_model=SimulationResult,
    summary="Simulate Path Traversal",
    description="Submits an LFI payload to demonstrate request inspection interception."
)
async def simulate_path_traversal(
    request: SimulationRequest,
    current_user: User = Depends(get_current_active_user),
    service: SimulationService = Depends(get_simulation_service)
):
    request.attack_type = AttackType.PATH_TRAVERSAL
    return await service.run_simulation(current_user, request)

@router.get(
    "/history",
    summary="Retrieve Simulation History",
    description="Queries the Audit Logs for all triggered ATTACK_DETECTED events."
)
async def get_simulation_history(
    service: SimulationService = Depends(get_simulation_service)
):
    return await service.get_simulation_history()
