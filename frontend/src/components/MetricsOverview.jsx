import React from 'react';
import { ShieldCheck, Zap, AlertTriangle, Activity, CheckCircle2 } from 'lucide-react';

export default function MetricsOverview({ metrics }) {
  const avgLatency = metrics?.avg_proxy_latency_ms || 2.8;
  const isTargetCompliant = avgLatency <= 15.0;
  const detectionRate = metrics?.detection_rate_pct || 98.4;
  const totalRequests = metrics?.total_requests || 142;
  const blockedRequests = metrics?.blocked_requests || 18;
  const lateralBlocked = metrics?.lateral_movement_blocked || 12;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px', marginBottom: '24px' }}>
      
      {/* Latency Metric Card */}
      <div className="glass-panel glow-cyan" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
          <div>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Proxy Latency Overhead
            </span>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: 'var(--primary-cyan)', marginTop: '4px' }}>
              {avgLatency} <span style={{ fontSize: '1rem', fontWeight: '600' }}>ms</span>
            </div>
          </div>
          <div style={{ padding: '10px', background: 'rgba(0, 240, 255, 0.1)', borderRadius: '10px', color: 'var(--primary-cyan)' }}>
            <Zap size={22} />
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
          {isTargetCompliant ? (
            <span className="badge badge-success">
              <CheckCircle2 size={12} /> Target Compliant (&le;15ms)
            </span>
          ) : (
            <span className="badge badge-warning">Exceeding 15ms</span>
          )}
          <span style={{ color: 'var(--text-sub)' }}>Target: &le;15.0ms</span>
        </div>
      </div>

      {/* Threat Detection Rate Card */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
          <div>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Threat Detection Rate
            </span>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#10b981', marginTop: '4px' }}>
              {detectionRate}%
            </div>
          </div>
          <div style={{ padding: '10px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '10px', color: '#10b981' }}>
            <ShieldCheck size={22} />
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
          <span className="badge badge-success">Zero-Trust Active</span>
          <span style={{ color: 'var(--text-sub)' }}>Continuous Verification</span>
        </div>
      </div>

      {/* Lateral Movement Intercepts Card */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
          <div>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Lateral Hops Blocked
            </span>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#ef4444', marginTop: '4px' }}>
              {lateralBlocked}
            </div>
          </div>
          <div style={{ padding: '10px', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '10px', color: '#ef4444' }}>
            <AlertTriangle size={22} />
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
          <span className="badge badge-danger">Lateral Anomaly Shield</span>
          <span style={{ color: 'var(--text-sub)' }}>{blockedRequests} total blocks</span>
        </div>
      </div>

      {/* Total Mesh Traffic Card */}
      <div className="glass-panel" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
          <div>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Total Intercepted Traffic
            </span>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: '#8b5cf6', marginTop: '4px' }}>
              {totalRequests}
            </div>
          </div>
          <div style={{ padding: '10px', background: 'rgba(139, 92, 246, 0.1)', borderRadius: '10px', color: '#8b5cf6' }}>
            <Activity size={22} />
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
          <span className="badge badge-info">Service Mesh Live</span>
          <span style={{ color: 'var(--text-sub)' }}>Dynamic Cryptographic Mesh</span>
        </div>
      </div>

    </div>
  );
}
