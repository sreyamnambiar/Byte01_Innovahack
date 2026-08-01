import React, { useState, useEffect } from 'react';
import { Sliders, Globe, Shield, HardDrive, Check, Save } from 'lucide-react';

export default function PolicyManager() {
  const [policies, setPolicies] = useState({
    allowed_geos: ['US', 'EU', 'IN', 'SG', 'JP'],
    max_payload_kb: 50.0,
    blocked_ips: ['192.168.1.99', '10.0.0.66'],
    time_restriction_enabled: false,
    rbac_matrix: {}
  });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetch('/api/policies')
      .then(res => res.json())
      .then(data => setPolicies(data))
      .catch(err => console.error(err));
  }, []);

  const handleSave = async () => {
    try {
      const res = await fetch('/api/policies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          allowed_geos: policies.allowed_geos,
          max_payload_kb: parseFloat(policies.max_payload_kb),
          blocked_ips: policies.blocked_ips
        })
      });
      if (res.ok) {
        setSaved(true);
        setTimeout(() => setSaved(false), 3000);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sliders size={22} color="var(--primary-cyan)" /> 🛡️ Contextual Zero-Trust Policy Engine
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Configure active zero-trust contextual evaluation rules (Time, Geolocation, Payload limits, IP Blacklists).
          </p>
        </div>

        <button className="btn-primary" onClick={handleSave} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          {saved ? <Check size={16} /> : <Save size={16} />} {saved ? 'Policy Applied!' : 'Save Active Policy'}
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
        
        {/* Geo-Fencing Rule */}
        <div className="glass-panel" style={{ padding: '18px', background: 'rgba(15, 23, 42, 0.5)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <Globe size={18} color="var(--primary-cyan)" />
            <h4 style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Geolocation Geo-Fence Rules
            </h4>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
            Permitted country codes for microservice API ingress:
          </p>
          <input 
            type="text"
            className="font-mono"
            style={{ width: '100%', padding: '10px', background: '#05070a', border: '1px solid var(--border-color)', color: 'var(--primary-cyan)', borderRadius: '6px', fontSize: '0.85rem' }}
            value={policies.allowed_geos.join(', ')}
            onChange={(e) => setPolicies({ ...policies, allowed_geos: e.target.value.split(',').map(s => s.trim()) })}
          />
        </div>

        {/* Payload Limit Rule */}
        <div className="glass-panel" style={{ padding: '18px', background: 'rgba(15, 23, 42, 0.5)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <HardDrive size={18} color="var(--accent-purple)" />
            <h4 style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Payload Size Anomaly Limit (KB)
            </h4>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
            Maximum allowed payload size per microservice call:
          </p>
          <input 
            type="number"
            className="font-mono"
            style={{ width: '100%', padding: '10px', background: '#05070a', border: '1px solid var(--border-color)', color: 'var(--accent-purple)', borderRadius: '6px', fontSize: '0.85rem' }}
            value={policies.max_payload_kb}
            onChange={(e) => setPolicies({ ...policies, max_payload_kb: e.target.value })}
          />
        </div>

        {/* IP Blacklist Rule */}
        <div className="glass-panel" style={{ padding: '18px', background: 'rgba(15, 23, 42, 0.5)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <Shield size={18} color="#ef4444" />
            <h4 style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--text-main)' }}>
              Blacklisted IP Fences
            </h4>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '12px' }}>
            Comma-separated IP addresses to instantly block:
          </p>
          <input 
            type="text"
            className="font-mono"
            style={{ width: '100%', padding: '10px', background: '#05070a', border: '1px solid var(--border-color)', color: '#ef4444', borderRadius: '6px', fontSize: '0.85rem' }}
            value={policies.blocked_ips.join(', ')}
            onChange={(e) => setPolicies({ ...policies, blocked_ips: e.target.value.split(',').map(s => s.trim()) })}
          />
        </div>

      </div>
    </div>
  );
}
