import time
import random
import hashlib
from typing import Dict, Any, List
from app.core.proxy import service_mesh_proxy
from app.core.crypto import crypto_engine

class AttackSimulationEngine:
    def __init__(self):
        pass

    def run_simulation(self, scenario_type: str) -> Dict[str, Any]:
        """
        Executes attack simulation vector and measures DarkTrust detection accuracy & proxy latency.
        """
        timestamp = time.time()
        
        if scenario_type == "LATERAL_MOVEMENT":
            # Scenario: Edge Gateway compromised; attacker tries direct jump to database-api bypassing user-service
            caller = "edge-gateway"
            target = "database-api"
            payload = {"query": "SELECT * FROM sensitive_user_credentials;"}
            payload_hash = hashlib.sha256(str(payload).encode()).hexdigest()[:16]
            # Attacker presents invalid/stale token for direct DB access
            token = "dt-v1.invalid_lateral_movement_claims.fake_sig"
            context = {
                "role": "edge-gateway",
                "client_ip": "10.0.4.15",
                "geo": "US",
                "payload_size_kb": 1.2,
                "action": "DB_SCRAPE_ATTEMPT"
            }
            desc = "Attacker compromised Edge Microservice and attempted unauthorized lateral hop directly to Database API."

        elif scenario_type == "TOKEN_REPLAY":
            caller = "user-service"
            target = "database-api"
            payload = {"user_id": 404}
            # Valid token expired 5 minutes ago
            token = "dt-v1.eyJpc3MiOiJ1c2VyLXNlcnZpY2UiLCJhdWQiOiJkYXRhYmFzZS1hcGkiLCJpYXQiOjE2MDAwMDAwMDAsImV4cCI6MTYwMDAwMDAzMH0=.expired_signature"
            context = {
                "role": "user-service",
                "client_ip": "10.0.2.11",
                "geo": "US",
                "payload_size_kb": 0.5,
                "action": "FETCH_USER"
            }
            desc = "Attacker replaying stolen expired dynamic token across microservice boundary."

        elif scenario_type == "GEO_SPOOFING":
            caller = "client"
            target = "edge-gateway"
            payload = {"action": "login"}
            token = crypto_engine.generate_service_token("edge-gateway", "client", "hash123")
            context = {
                "role": "guest",
                "client_ip": "185.220.101.5",
                "geo": "TOR", # Blocked location
                "payload_size_kb": 0.4,
                "action": "GEO_BYPASS_ATTEMPT"
            }
            desc = "Attacker routing traffic through TOR exit node from unauthorized location."

        elif scenario_type == "PAYLOAD_ANOMALY":
            caller = "analytics-service"
            target = "database-api"
            # Oversized exfiltration payload
            payload = {"data": "X" * 60000} # > 50KB limit
            payload_hash = hashlib.sha256(str(payload).encode()).hexdigest()[:16]
            token = crypto_engine.generate_service_token(target, caller, payload_hash)
            context = {
                "role": "analytics-service",
                "client_ip": "10.0.5.20",
                "geo": "US",
                "payload_size_kb": 62.5,
                "action": "EXFILTRATION_PAYLOAD"
            }
            desc = "Attacker attempting data exfiltration using oversized payload anomaly."

        elif scenario_type == "NORMAL_VERIFIED_REQUEST":
            caller = "user-service"
            target = "database-api"
            payload = {"action": "get_profile", "user_id": 101}
            payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16] if 'json' in locals() else "hash_normal"
            token = crypto_engine.generate_service_token(target, caller, payload_hash)
            context = {
                "role": "user-service",
                "client_ip": "10.0.2.10",
                "geo": "US",
                "payload_size_kb": 0.8,
                "action": "GET_PROFILE"
            }
            desc = "Legitimate microservice request with valid cryptographic identity and passed policy checks."

        else:
            return {"error": f"Unknown scenario: {scenario_type}"}

        # Evaluate through Zero-Trust Service Mesh Proxy
        is_allowed, reason, metrics = service_mesh_proxy.evaluate_request(
            caller_service=caller,
            target_service=target,
            token=token,
            context=context,
            payload=payload
        )

        return {
            "scenario": scenario_type,
            "description": desc,
            "blocked": not is_allowed,
            "decision_reason": reason,
            "status": metrics["status"],
            "risk_score": metrics["risk_score"],
            "proxy_latency_ms": metrics["proxy_latency_ms"],
            "crypto_valid": metrics["crypto_valid"],
            "anomalies_detected": metrics["anomalies"],
            "event_id": metrics["event_id"]
        }

attack_simulator = AttackSimulationEngine()
