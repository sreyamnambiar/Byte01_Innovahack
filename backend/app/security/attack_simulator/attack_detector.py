"""
DarkTrust – Attack Detector

A lightweight inspection engine that parses a given SimulationRequest 
against the attack_rules.py to identify the threat vector.
"""

from typing import Any
from app.security.attack_simulator.simulation_models import SimulationRequest, AttackType, AttackSeverity
from app.security.attack_simulator.attack_rules import ATTACK_SIGNATURES

class AttackDetector:
    
    @classmethod
    def analyze_payload(cls, payload: dict[str, Any] | None, expected_type: AttackType) -> tuple[bool, str | None, AttackSeverity]:
        """
        Scans a dictionary payload against regex signatures.
        Returns (is_detected, description, severity).
        """
        if not payload:
            # If no payload, but we're simulating behavioral attacks (like bruteforce), 
            # we default to True for the sake of the simulation flow.
            return True, "Behavioral attack triggered", AttackSeverity.MEDIUM
            
        signatures = ATTACK_SIGNATURES.get(expected_type)
        if not signatures:
            return True, f"Simulated {expected_type.value}", AttackSeverity.MEDIUM
            
        # Recursive check if payload has nested dicts
        def scan_dict(d: dict):
            for v in d.values():
                if isinstance(v, dict):
                    if scan_dict(v):
                        return True
                elif isinstance(v, str):
                    for pattern in signatures["patterns"]:
                        if pattern.search(v):
                            return True
            return False
            
        if scan_dict(payload):
            return True, signatures["description"], signatures["severity"]
            
        # If payload didn't match regex but the user requested the simulation, 
        # we trigger it anyway for demonstration.
        return True, f"Forced simulation of {expected_type.value}", signatures.get("severity", AttackSeverity.MEDIUM)
