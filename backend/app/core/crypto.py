import time
import hmac
import hashlib
import json
import base64
from typing import Dict, Any, Tuple
from app.core.config import settings

class CryptographicIdentityEngine:
    def __init__(self, secret_key: str = settings.SECRET_KEY):
        self.secret_key = secret_key.encode('utf-8')

    def generate_service_token(self, service_id: str, caller_id: str, payload_hash: str) -> str:
        """
        Generates a dynamic, short-lived microservice identity token signed cryptographically.
        Includes timestamp, caller_id, target service_id, and payload_hash.
        """
        now = time.time()
        claims = {
            "iss": caller_id,
            "aud": service_id,
            "phash": payload_hash,
            "iat": now,
            "exp": now + 30, # Ephemeral 30s TTL
            "nonce": hashlib.sha256(f"{now}:{caller_id}:{service_id}".encode()).hexdigest()[:16]
        }
        encoded_claims = base64.b64encode(json.dumps(claims).encode()).decode()
        signature = hmac.new(self.secret_key, encoded_claims.encode(), hashlib.sha256).hexdigest()
        return f"dt-v1.{encoded_claims}.{signature}"

    def verify_service_token(self, token: str, expected_target_service: str, payload: Any = None) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validates cryptographic service token, expiration, signature, and payload integrity.
        Returns (is_valid, reason, claims).
        """
        if not token or not token.startswith("dt-v1."):
            return False, "Invalid token format", {}

        parts = token.split(".")
        if len(parts) != 3:
            return False, "Malformed token structure", {}

        _, encoded_claims, signature = parts
        expected_sig = hmac.new(self.secret_key, encoded_claims.encode(), hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(signature, expected_sig):
            return False, "Cryptographic signature verification failed", {}

        try:
            claims = json.loads(base64.b64decode(encoded_claims.encode()).decode())
        except Exception:
            return False, "Failed to decode claim payload", {}

        now = time.time()
        if now > claims.get("exp", 0):
            return False, "Ephemeral token expired", claims

        if claims.get("aud") != expected_target_service:
            return False, f"Audience mismatch: expected {expected_target_service}, got {claims.get('aud')}", claims

        if payload is not None:
            calc_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
            if claims.get("phash") != calc_hash:
                return False, "Payload tampering detected (hash mismatch)", claims

        return True, "Valid cryptographic identity", claims

crypto_engine = CryptographicIdentityEngine()
