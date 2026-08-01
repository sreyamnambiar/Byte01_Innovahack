"""
DarkTrust – Simulation Service

Business logic layer for executing and retrieving simulation records.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.security.attack_simulator.simulator import AttackSimulator
from app.security.attack_simulator.simulation_models import SimulationRequest, SimulationResult
from app.services.audit_service import AuditService
from app.models.audit_log import AuditEventType

class SimulationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.audit_service = AuditService(session)

    async def run_simulation(self, user: User, request: SimulationRequest) -> SimulationResult:
        """Executes a simulation payload."""
        return await AttackSimulator.simulate_attack(self.session, user, request)

    async def get_simulation_history(self) -> list:
        """Retrieves history of simulated attacks from the Audit Logs."""
        return await self.audit_service.get_logs_by_event(AuditEventType.ATTACK_DETECTED)
