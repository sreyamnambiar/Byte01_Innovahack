import pytest
import time
from app.core.crypto import crypto_engine
from app.core.policy_engine import policy_engine
from app.core.risk_engine import risk_engine
from app.core.proxy import service_mesh_proxy
from app.core.simulator import attack_simulator

def test_proxy_latency_overhead_under_15ms():
    """Verify that proxy overhead latency remains <= 15ms target."""
    token = crypto_engine.generate_service_token("user-service", "edge-gateway", "hash123")
    context = {"role": "edge-gateway", "client_ip": "10.0.0.1", "geo": "US", "payload_size_kb": 1.0}
    
    start = time.perf_counter()
    allowed, reason, metrics = service_mesh_proxy.evaluate_request(
        caller_service="edge-gateway",
        target_service="user-service",
        token=token,
        context=context
    )
    duration_ms = (time.perf_counter() - start) * 1000.0

    assert duration_ms <= 15.0, f"Proxy latency ({duration_ms:.2f}ms) exceeded 15ms target"
    assert metrics["proxy_latency_ms"] <= 15.0

def test_cryptographic_identity_validation():
    """Test dynamic ephemeral service token issuance and verification."""
    payload = {"data": "test_payload"}
    payload_hash = "abc123hash"
    token = crypto_engine.generate_service_token("database-api", "user-service", payload_hash)

    # Valid verification
    valid, reason, claims = crypto_engine.verify_service_token(token, "database-api")
    assert valid is True
    assert claims["iss"] == "user-service"
    assert claims["aud"] == "database-api"

    # Mismatched audience verification
    invalid, reason_bad_aud, _ = crypto_engine.verify_service_token(token, "wrong-service")
    assert invalid is False
    assert "Audience mismatch" in reason_bad_aud

def test_lateral_movement_detection():
    """Test that unauthorized lateral hops (e.g. Edge directly jumping to DB) raise high risk."""
    context = {"role": "edge-gateway", "client_ip": "10.0.0.5", "geo": "US"}
    risk_score, anomalies = risk_engine.evaluate_risk(
        caller_service="edge-gateway",
        target_service="database-api",
        context=context,
        crypto_valid=False
    )
    assert risk_score >= 45.0
    assert any("LATERAL MOVEMENT DETECTED" in a for a in anomalies)

def test_attack_simulator_scenarios():
    """Test attack simulation vectors."""
    result = attack_simulator.run_simulation("LATERAL_MOVEMENT")
    assert result["scenario"] == "LATERAL_MOVEMENT"
    assert result["blocked"] is True
    assert result["risk_score"] > 50.0

    result_normal = attack_simulator.run_simulation("NORMAL_VERIFIED_REQUEST")
    assert result_normal["blocked"] is False
    assert result_normal["crypto_valid"] is True
