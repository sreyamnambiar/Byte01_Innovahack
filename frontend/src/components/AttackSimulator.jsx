import React, { useState } from 'react';
import { Play, ShieldAlert, Zap, AlertCircle, CheckCircle2, Lock } from 'lucide-react';

export default function AttackSimulator({ onRunSimulation }) {
  const [loading, setLoading] = useState(false);
  const [lastResult, setLastResult] = useState(null);

  const scenarios = [
    {
      id: 'LATERAL_MOVEMENT',
      title: '🚨 Edge Microservice Compromise & Lateral Hop',
      description: 'Attacker breaches Edge Gateway and attempts a direct lateral jump to Database API bypassing User Service.',
      badge: 'High Severity',
      badgeClass: 'badge-danger'
    },
    {
      id: 'TOKEN_REPLAY',
      title: '🔑 Token Theft & Stale Ephemeral Replay',
      description: 'Attacker captures a stale 30s microservice token and attempts to replay it against backend endpoints.',
      badge: 'Crypto Fail',
      badgeClass: 'badge-warning'
    },
    {
      id: 'GEO_SPOOFING',
      title: '🌐 Anonymous TOR Exit Node Geo-Fence Bypass',
      description: 'Attacker routes requests through anonymized TOR nodes to bypass geolocation zero-trust policies.',
      badge: 'Geo Violation',
      badgeClass: 'badge-warning'
    },
    {
      id: 'PAYLOAD_ANOMALY',
      title: '📦 Large Data Exfiltration Payload Anomaly',
      description: 'Attacker injects a massive 62KB exfiltration payload exceeding the 50KB zero-trust policy threshold.',
      badge: 'Payload Anomaly',
      badgeClass: 'badge-danger'
    },
    {
      id: 'NORMAL_VERIFIED_REQUEST',
      title: '✅ Legitimate Authenticated Microservice Request',
      description: 'User-Service requests Database API using a valid cryptographic HMAC signature and valid context.',
      badge: 'Valid Flow',
      badgeClass: 'badge-success'
    }
  ];

  const handleRun = async (scenarioId) => {
    setLoading(true);
    try {
      const res = await fetch('/api/attack-sim/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario: scenarioId })
      });
      const data = await res.json();
      setLastResult(data);
      if (onRunSimulation) onRunSimulation(data);
    } catch (err) {
      console.error("Simulation error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ShieldAlert color="#ef4444" size={24} /> ⚡ Zero-Trust Attack Simulation & Threat Breach Studio
        </h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
          Trigger simulated cyber attack vectors to evaluate DarkTrust proxy latency, lateral movement detection, and threat mitigation response.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        {scenarios.map((sc) => (
          <div key={sc.id} className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', background: 'rgba(15, 23, 42, 0.5)' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                <span className={`badge ${sc.badgeClass}`}>{sc.badge}</span>
              </div>
              <h4 style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--text-main)', marginBottom: '6px' }}>
                {sc.title}
              </h4>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                {sc.description}
              </p>
            </div>
            
            <button 
              className={sc.id === 'NORMAL_VERIFIED_REQUEST' ? 'btn-primary' : 'btn-danger'} 
              style={{ marginTop: '16px', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', fontSize: '0.85rem' }}
              disabled={loading}
              onClick={() => handleRun(sc.id)}
            >
              <Play size={14} /> {loading ? 'Evaluating...' : 'Launch Attack Vector'}
            </button>
          </div>
        ))}
      </div>

      {/* Live Simulation Response Telemetry Card */}
      {lastResult && (
        <div className="glass-panel" style={{ padding: '20px', background: lastResult.blocked ? 'rgba(239, 68, 68, 0.08)' : 'rgba(16, 185, 129, 0.08)', border: lastResult.blocked ? '1px solid rgba(239, 68, 68, 0.3)' : '1px solid rgba(16, 185, 129, 0.3)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              {lastResult.blocked ? (
                <ShieldAlert size={26} color="#ef4444" />
              ) : (
                <CheckCircle2 size={26} color="#10b981" />
              )}
              <div>
                <h4 style={{ fontSize: '1.05rem', fontWeight: '800', color: lastResult.blocked ? '#ef4444' : '#10b981' }}>
                  Proxy Decision: {lastResult.status} ({lastResult.blocked ? 'ACCESS BLOCKED' : 'ACCESS ALLOWED'})
                </h4>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  Scenario: {lastResult.scenario}
                </span>
              </div>
            </div>

            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--primary-cyan)' }}>
                {lastResult.proxy_latency_ms} ms
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-sub)' }}>Proxy Latency Overhead</span>
            </div>
          </div>

          <p style={{ fontSize: '0.85rem', color: 'var(--text-main)', marginBottom: '12px', background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '6px' }}>
            <strong>Reason:</strong> {lastResult.decision_reason}
          </p>

          {/* Anomaly list */}
          {lastResult.anomalies_detected && lastResult.anomalies_detected.length > 0 && (
            <div>
              <span style={{ fontSize: '0.8rem', fontWeight: '700', color: '#ef4444', display: 'block', marginBottom: '6px' }}>
                ⚠️ Anomaly Threat Signals Detected:
              </span>
              <ul style={{ paddingLeft: '20px', fontSize: '0.8rem', color: '#f87171' }}>
                {lastResult.anomalies_detected.map((an, idx) => (
                  <li key={idx} style={{ marginBottom: '4px' }}>{an}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
