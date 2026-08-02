import React, { useState } from 'react';
import { Send, Zap, Key } from 'lucide-react';

export default function ProxyTester({ onTestComplete }) {
  const [caller, setCaller] = useState('user-service');
  const [target, setTarget] = useState('database-api');
  const [role, setRole] = useState('user-service');
  const [geo, setGeo] = useState('US');
  const [payloadSize, setPayloadSize] = useState(1.5);
  const [clientIp, setClientIp] = useState('10.0.2.14');
  
  const [token, setToken] = useState('');
  const [evalResult, setEvalResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateToken = async () => {
    try {
      const res = await fetch('/api/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ caller_service: caller, target_service: target })
      });
      const data = await res.json();
      setToken(data.token);
    } catch (err) {
      console.error(err);
    }
  };

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      let currentToken = token;
      if (!currentToken) {
        const tokenRes = await fetch('/api/auth/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ caller_service: caller, target_service: target })
        });
        const tokenData = await tokenRes.json();
        currentToken = tokenData.token;
        setToken(currentToken);
      }

      const res = await fetch('/api/proxy/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          caller_service: caller,
          target_service: target,
          token: currentToken,
          role: role,
          client_ip: clientIp,
          geo: geo,
          payload_size_kb: parseFloat(payloadSize)
        })
      });
      const data = await res.json();
      setEvalResult(data);
      if (onTestComplete) onTestComplete(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Zap size={22} color="var(--primary-cyan)" /> ⚡ Custom Service Mesh Proxy Request Interceptor
        </h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
          Simulate arbitrary microservice calls and measure exact proxy overhead latency (&le;15ms target) and zero-trust evaluation.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px', marginBottom: '20px' }}>
        
        <div>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>Caller Microservice</label>
          <select 
            style={{ width: '100%', padding: '10px', background: 'var(--input-bg)', border: '1px solid var(--input-border)', color: 'var(--text-main)', borderRadius: '6px', fontSize: '0.85rem' }}
            value={caller} 
            onChange={e => {
              setCaller(e.target.value);
              setRole(e.target.value);
            }}
          >
            <option value="edge-gateway">edge-gateway</option>
            <option value="auth-service">auth-service</option>
            <option value="user-service">user-service</option>
            <option value="analytics-service">analytics-service</option>
            <option value="guest">guest-client</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>Target Microservice</label>
          <select 
            style={{ width: '100%', padding: '10px', background: 'var(--input-bg)', border: '1px solid var(--input-border)', color: 'var(--text-main)', borderRadius: '6px', fontSize: '0.85rem' }}
            value={target} 
            onChange={e => setTarget(e.target.value)}
          >
            <option value="database-api">database-api</option>
            <option value="user-service">user-service</option>
            <option value="auth-service">auth-service</option>
            <option value="analytics-service">analytics-service</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>Geolocation Region</label>
          <select 
            style={{ width: '100%', padding: '10px', background: 'var(--input-bg)', border: '1px solid var(--input-border)', color: 'var(--text-main)', borderRadius: '6px', fontSize: '0.85rem' }}
            value={geo} 
            onChange={e => setGeo(e.target.value)}
          >
            <option value="US">US (United States)</option>
            <option value="EU">EU (Europe)</option>
            <option value="IN">IN (India)</option>
            <option value="TOR">TOR (Anonymous Proxy)</option>
            <option value="CN">CN (Restricted)</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>Payload Size (KB)</label>
          <input 
            type="number" 
            style={{ width: '100%', padding: '10px', background: 'var(--input-bg)', border: '1px solid var(--input-border)', color: 'var(--text-main)', borderRadius: '6px', fontSize: '0.85rem' }}
            value={payloadSize} 
            onChange={e => setPayloadSize(e.target.value)} 
          />
        </div>

      </div>

      <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
        <button className="btn-secondary" onClick={handleGenerateToken} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Key size={14} /> Generate Ephemeral Token
        </button>
        <button className="btn-primary" onClick={handleEvaluate} disabled={loading} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Send size={14} /> {loading ? 'Intercepting...' : 'Send Through Proxy'}
        </button>
      </div>

      {token && (
        <div style={{ fontSize: '0.75rem', fontFamily: 'monospace', color: 'var(--primary-cyan)', background: 'var(--input-bg)', border: '1px solid var(--input-border)', padding: '8px 12px', borderRadius: '6px', marginBottom: '16px', overflowX: 'auto' }}>
          Token: {token}
        </div>
      )}

      {evalResult && (
        <div className="glass-panel" style={{ padding: '16px', background: evalResult.allowed ? 'rgba(16, 185, 129, 0.08)' : 'rgba(239, 68, 68, 0.08)', border: evalResult.allowed ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontWeight: '700', color: evalResult.allowed ? 'var(--status-success)' : 'var(--status-danger)' }}>
              {evalResult.allowed ? '✅ PERMITTED BY PROXY' : '❌ BLOCKED BY PROXY'} - Risk: {evalResult.metrics.risk_score}/100
            </span>
            <span className="font-mono" style={{ color: 'var(--primary-cyan)', fontWeight: '700' }}>
              Overhead: {evalResult.metrics.proxy_latency_ms} ms
            </span>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-main)', marginTop: '6px' }}>
            {evalResult.reason}
          </p>
        </div>
      )}
    </div>
  );
}
