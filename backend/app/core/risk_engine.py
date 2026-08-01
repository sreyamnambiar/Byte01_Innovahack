import time
from typing import Dict, Any, List, Tuple

class AdaptiveRiskEngine:
    def __init__(self):
        # Recent request history for frequency & anomaly calculation
        self.request_history: List[Dict[str, Any]] = []
        # Valid topological service call chains (caller -> target)
        self.valid_topology_hops = {
            ("client", "edge-gateway"),
            ("edge-gateway", "auth-service"),
            ("edge-gateway", "user-service"),
            ("edge-gateway", "analytics-service"),
            ("auth-service", "user-service"),
            ("user-service", "database-api"),
            ("analytics-service", "database-api"),
        }

    def evaluate_risk(self, caller_service: str, target_service: str, context: Dict[str, Any], crypto_valid: bool) -> Tuple[float, List[str]]:
        """
        Calculates dynamic risk score (0-100) and identifies lateral movement / anomaly threat vectors.
        """
        risk_score = 0.0
        anomalies: List[str] = []

        # 1. Lateral Movement Check: Direct jump bypassing architecture
        hop_pair = (caller_service, target_service)
        if hop_pair not in self.valid_topology_hops and caller_service != "admin":
            risk_score += 45.0
            anomalies.append(f"LATERAL MOVEMENT DETECTED: Direct hop '{caller_service}' ➔ '{target_service}' bypasses security boundary")

        # 2. Cryptographic Token Status
        if not crypto_valid:
            risk_score += 35.0
            anomalies.append("CRYPTOGRAPHIC IDENTITY INVALID: Unverified token or hash mismatch")

        # 3. Geo Anomaly
        geo = context.get("geo", "UNKNOWN").upper()
        if geo in ["TOR", "ANONYMOUS", "RU", "CN"]:
            risk_score += 25.0
            anomalies.append(f"HIGH RISK LOCATION: Request originated from untrusted region '{geo}'")

        # 4. Request Rate / High Frequency Scraping Anomaly
        now = time.time()
        client_ip = context.get("client_ip", "0.0.0.0")
        recent_calls = [r for r in self.request_history if r["client_ip"] == client_ip and now - r["time"] < 10.0]
        if len(recent_calls) > 15:
            risk_score += 30.0
            anomalies.append(f"SCRAPING / RATE ANOMALY: High request frequency ({len(recent_calls)} reqs / 10s) detected")

        # 5. Payload Size Anomaly
        payload_kb = context.get("payload_size_kb", 0.0)
        if payload_kb > 30.0:
            risk_score += 15.0
            anomalies.append(f"PAYLOAD ANOMALY: Large payload size ({payload_kb:.1f} KB) detected")

        # Cap risk score between 0 and 100
        final_risk_score = min(100.0, max(0.0, risk_score))

        # Store in history
        self.request_history.append({
            "caller": caller_service,
            "target": target_service,
            "client_ip": client_ip,
            "time": now,
            "risk": final_risk_score
        })
        # Prune old history
        if len(self.request_history) > 200:
            self.request_history = self.request_history[-200:]

        return final_risk_score, anomalies

risk_engine = AdaptiveRiskEngine()
