import datetime
from typing import Dict, Any, List, Tuple

class ZeroTrustPolicyEngine:
    def __init__(self):
        # Default policies
        self.allowed_geos = ["US", "EU", "IN", "SG", "JP"]
        self.blocked_ips = ["192.168.1.99", "10.0.0.66", "172.16.0.404"]
        self.max_payload_kb = 50.0  # Max 50KB
        self.time_restriction_enabled = False
        
        # RBAC Table: Role -> allowed target endpoints
        self.rbac_matrix: Dict[str, List[str]] = {
            "admin": ["*"],
            "edge-gateway": ["auth-service", "user-service", "analytics-service"],
            "auth-service": ["user-service"],
            "user-service": ["database-api"],
            "analytics-service": ["database-api"],
            "guest": ["public-info"]
        }

    def evaluate_context(self, context: Dict[str, Any], target_service: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Evaluates dynamic contextual policies.
        Context expected keys: role, client_ip, geo, payload_size_kb, timestamp.
        """
        eval_details = {
            "geo_check": "PASS",
            "ip_check": "PASS",
            "payload_check": "PASS",
            "rbac_check": "PASS",
            "time_check": "PASS"
        }

        # 1. IP Blacklist check
        client_ip = context.get("client_ip", "0.0.0.0")
        if client_ip in self.blocked_ips:
            eval_details["ip_check"] = "FAIL"
            return False, f"Client IP {client_ip} is blacklisted", eval_details

        # 2. Geolocation fencing check
        geo = context.get("geo", "UNKNOWN").upper()
        if geo not in self.allowed_geos and geo != "LOCAL":
            eval_details["geo_check"] = "FAIL"
            return False, f"Geolocation '{geo}' violates zero-trust geo-fence policy", eval_details

        # 3. Payload size restriction
        payload_size_kb = context.get("payload_size_kb", 0.0)
        if payload_size_kb > self.max_payload_kb:
            eval_details["payload_check"] = "FAIL"
            return False, f"Payload size ({payload_size_kb:.1f} KB) exceeds policy limit ({self.max_payload_kb} KB)", eval_details

        # 4. RBAC Permission check
        caller_role = context.get("role", "guest")
        allowed_targets = self.rbac_matrix.get(caller_role, [])
        if "*" not in allowed_targets and target_service not in allowed_targets:
            eval_details["rbac_check"] = "FAIL"
            return False, f"Role '{caller_role}' unauthorized to access target microservice '{target_service}'", eval_details

        # 5. Time-based access check (if enabled)
        if self.time_restriction_enabled:
            current_hour = datetime.datetime.now().hour
            if current_hour < 6 or current_hour > 22: # Allow 06:00 to 22:00
                eval_details["time_check"] = "FAIL"
                return False, "Access denied: Outside permitted operational hours (06:00 - 22:00)", eval_details

        return True, "All contextual zero-trust policies passed", eval_details

    def update_policy(self, allowed_geos: List[str] = None, max_payload_kb: float = None, blocked_ips: List[str] = None):
        if allowed_geos is not None:
            self.allowed_geos = [g.upper() for g in allowed_geos]
        if max_payload_kb is not None:
            self.max_payload_kb = max_payload_kb
        if blocked_ips is not None:
            self.blocked_ips = blocked_ips

policy_engine = ZeroTrustPolicyEngine()
