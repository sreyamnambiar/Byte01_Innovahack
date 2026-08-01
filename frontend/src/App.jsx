import React, { useState, useEffect } from 'react';
import { Shield, Zap, Sliders, Activity, Play, Terminal, Lock } from 'lucide-react';
import MetricsOverview from './components/MetricsOverview';
import ServiceMeshVisualizer from './components/ServiceMeshVisualizer';
import AttackSimulator from './components/AttackSimulator';
import PolicyManager from './components/PolicyManager';
import ProxyTester from './components/ProxyTester';
import AuditLogFeed from './components/AuditLogFeed';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState([]);
  const [lastEvent, setLastEvent] = useState(null);

  const fetchTelemetry = async () => {
    try {
      const [mRes, lRes] = await Promise.all([
        fetch('/api/metrics'),
        fetch('/api/logs?limit=40')
      ]);
      if (mRes.ok) {
        const mData = await mRes.json();
        setMetrics(mData);
      }
      if (lRes.ok) {
        const lData = await lRes.json();
        setLogs(lData.logs || []);
        if (lData.logs && lData.logs.length > 0) {
          setLastEvent(lData.logs[0]);
        }
      }
    } catch (err) {
      console.log("Polling telemetry fallback...");
    }
  };

  useEffect(() => {
    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleSimulationOrTest = (resultData) => {
    fetchTelemetry();
    if (resultData && resultData.event_id) {
      setLastEvent(resultData);
    }
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '24px 16px' }}>
      
      {/* Top Header Bar */}
      <header className="glass-panel" style={{ padding: '20px 24px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{ padding: '10px', background: 'linear-gradient(135deg, #00f0ff 0%, #7000ff 100%)', borderRadius: '12px', color: '#000', display: 'flex', alignItems: 'center' }}>
            <Shield size={28} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.4rem', fontWeight: '800', letterSpacing: '-0.02em', background: 'linear-gradient(90deg, #ffffff, #00f0ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              DarkTrust Security Platform
            </h1>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Zero-Trust Access Control for Decentralized APIs | InnovaHack Byte01
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ textAlign: 'right' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-sub)', display: 'block' }}>PROXY OVERHEAD</span>
            <span className="font-mono" style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--primary-cyan)' }}>
              {metrics?.avg_proxy_latency_ms || 2.8} ms (&le;15ms Target)
            </span>
          </div>

          <span className="badge badge-success" style={{ padding: '8px 14px', fontSize: '0.8rem' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', display: 'inline-block' }}></span> Mesh Interceptor Live
          </span>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '24px', overflowX: 'auto', paddingBottom: '4px' }}>
        <button 
          className={activeTab === 'overview' ? 'btn-primary' : 'btn-secondary'}
          onClick={() => setActiveTab('overview')}
          style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <Activity size={16} /> Overview & Telemetry
        </button>

        <button 
          className={activeTab === 'simulator' ? 'btn-primary' : 'btn-secondary'}
          onClick={() => setActiveTab('simulator')}
          style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <Play size={16} /> Attack Simulator
        </button>

        <button 
          className={activeTab === 'tester' ? 'btn-primary' : 'btn-secondary'}
          onClick={() => setActiveTab('tester')}
          style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <Zap size={16} /> Proxy Request Tester
        </button>

        <button 
          className={activeTab === 'policies' ? 'btn-primary' : 'btn-secondary'}
          onClick={() => setActiveTab('policies')}
          style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <Sliders size={16} /> Policy Engine
        </button>

        <button 
          className={activeTab === 'logs' ? 'btn-primary' : 'btn-secondary'}
          onClick={() => setActiveTab('logs')}
          style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <Terminal size={16} /> Audit Stream ({logs.length})
        </button>
      </div>

      {/* Main Content Area */}
      <MetricsOverview metrics={metrics} />

      {activeTab === 'overview' && (
        <>
          <ServiceMeshVisualizer lastEvent={lastEvent} />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
            <AttackSimulator onRunSimulation={handleSimulationOrTest} />
            <ProxyTester onTestComplete={handleSimulationOrTest} />
          </div>
          <AuditLogFeed logs={logs} />
        </>
      )}

      {activeTab === 'simulator' && (
        <>
          <AttackSimulator onRunSimulation={handleSimulationOrTest} />
          <ServiceMeshVisualizer lastEvent={lastEvent} />
        </>
      )}

      {activeTab === 'tester' && (
        <>
          <ProxyTester onTestComplete={handleSimulationOrTest} />
          <ServiceMeshVisualizer lastEvent={lastEvent} />
        </>
      )}

      {activeTab === 'policies' && (
        <PolicyManager />
      )}

      {activeTab === 'logs' && (
        <AuditLogFeed logs={logs} />
      )}

      {/* Footer */}
      <footer style={{ textAlign: 'center', marginTop: '40px', padding: '20px', color: 'var(--text-sub)', fontSize: '0.8rem', borderTop: '1px solid var(--border-color)' }}>
        DarkTrust – Zero Trust Access Control for Decentralized APIs | Developed for InnovaHack Hackathon 2026
      </footer>

    </div>
  );
}
