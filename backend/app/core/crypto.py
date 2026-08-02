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
        # In-memory user database seed
        self.users_db: Dict[str, Dict[str, Any]] = {
            "admin@darktrust.io": {
                "id": "usr-1",
                "email": "admin@darktrust.io",
                "name": "Security Admin",
                "password_hash": self._hash_password("admin123"),
                "role": "admin"
            },
            "engineer@darktrust.io": {
                "id": "usr-2",
                "email": "engineer@darktrust.io",
                "name": "Security Engineer",
                "password_hash": self._hash_password("engineer123"),
                "role": "edge-gateway"
            }
        }

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256((password + settings.SECRET_KEY).encode()).hexdigest()

    def register_user(self, email: str, password: str, name: str, role: str = "guest") -> Tuple[bool, str, Dict[str, Any]]:
        if email in self.users_db:
            return False, "User with this email already exists", {}
        
        user_data = {
            "id": f"usr-{len(self.users_db)+1}",
            "email": email,
            "name": name,
            "password_hash": self._hash_password(password),
            "role": role
        }
        self.users_db[email] = user_data
        return True, "User registered successfully", {"id": user_data["id"], "email": email, "name": name, "role": role}

    def authenticate_user(self, email: str, password: str) -> Tuple[bool, str, str, Dict[str, Any]]:
        user = self.users_db.get(email)
        if not user:
            return False, "Invalid email or password", "", {}
        
        if user["password_hash"] != self._hash_password(password):
            return False, "Invalid email or password", "", {}

        # Issue user JWT token
        payload_hash = hashlib.sha256(email.encode()).hexdigest()[:16]
        token = self.generate_service_token(service_id="darktrust-dashboard", caller_id=user["id"], payload_hash=payload_hash)
        
        user_info = {"id": user["id"], "email": user["email"], "name": user["name"], "role": user["role"]}
        return True, "Authentication successful", token, user_info

    def generate_service_token(self, service_id: str, caller_id: str, payload_hash: str) -> str:
        now = time.time()
        claims = {
            "iss": caller_id,
            "aud": service_id,
            "phash": payload_hash,
            "iat": now,
            "exp": now + 3600, # 1 hour session TTL
            "nonce": hashlib.sha256(f"{now}:{caller_id}:{service_id}".encode()).hexdigest()[:16]
        }
        encoded_claims = base64.b64encode(json.dumps(claims).encode()).decode()
        signature = hmac.new(self.secret_key, encoded_claims.encode(), hashlib.sha256).hexdigest()
        return f"dt-v1.{encoded_claims}.{signature}"

    def verify_service_token(self, token: str, expected_target_service: str, payload: Any = None) -> Tuple[bool, str, Dict[str, Any]]:
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
            return False, "Token expired", claims

        if expected_target_service != "*" and claims.get("aud") != expected_target_service and claims.get("aud") != "darktrust-dashboard":
            return False, f"Audience mismatch: expected {expected_target_service}, got {claims.get('aud')}", claims

        if payload is not None:
            calc_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
            if claims.get("phash") != calc_hash:
                return False, "Payload tampering detected (hash mismatch)", claims

        return True, "Valid cryptographic identity", claims

crypto_engine = CryptographicIdentityEngine()
