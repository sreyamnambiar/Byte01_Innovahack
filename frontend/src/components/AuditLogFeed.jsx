import React from 'react';
import { Activity, ShieldAlert, ShieldCheck, Clock } from 'lucide-react';

export default function AuditLogFeed({ logs }) {
  const logItems = logs || [];

  return (
    <div className="glass-panel" style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Activity size={22} color="var(--accent-purple)" /> 📜 Real-Time Security Audit Log Stream
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Continuous zero-trust request telemetry, proxy latency records, and anomaly detections.
          </p>
        </div>

        <span className="badge badge-info">
          <Clock size={12} /> Live Streaming ({logItems.length} Events)
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '420px', overflowY: 'auto' }}>
        {logItems.length === 0 ? (
          <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-muted)' }}>
            No audit events logged yet. Launch an attack vector or proxy test.
          </div>
        ) : (
          logItems.map((evt) => {
            const isBlocked = evt.status === 'BLOCKED' || evt.status === 'DENIED';
            const isChallenged = evt.status === 'CHALLENGED_REAUTH';

            return (
              <div 
                key={evt.id} 
                className="glass-panel" 
                style={{ 
                  padding: '12px 16px', 
                  background: isBlocked ? 'rgba(239, 68, 68, 0.05)' : isChallenged ? 'rgba(245, 158, 11, 0.05)' : 'rgba(15, 23, 42, 0.4)',
                  borderLeft: isBlocked ? '4px solid #ef4444' : isChallenged ? '4px solid #f59e0b' : '4px solid #10b981'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span className="font-mono" style={{ fontSize: '0.8rem', color: 'var(--text-sub)' }}>
                      {evt.timestamp}
                    </span>

                    <div style={{ fontSize: '0.9rem', fontWeight: '700', color: 'var(--text-main)' }}>
                      <span style={{ color: 'var(--primary-cyan)' }}>{evt.caller}</span>
                      <span style={{ margin: '0 6px', color: 'var(--text-sub)' }}>➔</span>
                      <span style={{ color: 'var(--accent-purple)' }}>{evt.target}</span>
                    </div>

                    <span className={isBlocked ? 'badge badge-danger' : isChallenged ? 'badge badge-warning' : 'badge badge-success'}>
                      {evt.status}
                    </span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '0.85rem' }}>
                    <span style={{ color: evt.risk_score > 50 ? '#ef4444' : '#34d399', fontWeight: '700' }}>
                      Risk: {evt.risk_score}/100
                    </span>

                    <span className="font-mono" style={{ color: 'var(--primary-cyan)', fontWeight: '600' }}>
                      {evt.latency_ms} ms
                    </span>
                  </div>
                </div>

                {evt.anomalies && evt.anomalies.length > 0 && (
                  <div style={{ marginTop: '8px', fontSize: '0.78rem', color: '#f87171', background: 'rgba(0,0,0,0.3)', padding: '6px 10px', borderRadius: '4px' }}>
                    ⚠️ {evt.anomalies.join(' | ')}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
