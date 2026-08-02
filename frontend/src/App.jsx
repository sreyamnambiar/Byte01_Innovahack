import React, { useState, useEffect } from 'react';
import { Shield, Zap, Sliders, Activity, Play, Terminal, Lock, Sun, Moon, LogIn, LogOut, UserCheck } from 'lucide-react';
import MetricsOverview from './components/MetricsOverview';
import ServiceMeshVisualizer from './components/ServiceMeshVisualizer';
import AttackSimulator from './components/AttackSimulator';
import PolicyManager from './components/PolicyManager';
import ProxyTester from './components/ProxyTester';
import AuditLogFeed from './components/AuditLogFeed';
import AuthModal from './components/AuthModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [theme, setTheme] = useState(() => localStorage.getItem('darktrust-theme') || 'dark');
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState([]);
  const [lastEvent, setLastEvent] = useState(null);
  
  // Auth state
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('darktrust-user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem('darktrust-token') || '');
  const [isAuthOpen, setIsAuthOpen] = useState(false);

  // Synchronize Theme Attribute
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('darktrust-theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  const handleAuthSuccess = (userData, accessToken) => {
    setUser(userData);
    setToken(accessToken);
    localStorage.setItem('darktrust-user', JSON.stringify(userData));
    localStorage.setItem('darktrust-token', accessToken);
  };

  const handleLogout = () => {
    setUser(null);
    setToken('');
    localStorage.removeItem('darktrust-user');
    localStorage.removeItem('darktrust-token');
  };

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
          <div style={{ padding: '10px', background: 'linear-gradient(135deg, var(--primary-cyan) 0%, var(--accent-purple) 100%)', borderRadius: '12px', color: '#fff', display: 'flex', alignItems: 'center' }}>
            <Shield size={28} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.4rem', fontWeight: '800', letterSpacing: '-0.02em', color: 'var(--text-main)' }}>
              DarkTrust Security Platform
            </h1>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Zero-Trust Access Control for Decentralized APIs | InnovaHack Byte01
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          
          {/* Latency Meter */}
          <div style={{ textAlign: 'right', display: 'none', md: 'block' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-sub)', display: 'block' }}>PROXY OVERHEAD</span>
            <span className="font-mono" style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--primary-cyan)' }}>
              {metrics?.avg_proxy_latency_ms || 2.8} ms (&le;15ms Target)
            </span>
          </div>

          {/* Light / Dark Mode Toggle */}
          <button 
            className="btn-secondary" 
            onClick={toggleTheme}
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
            style={{ padding: '8px 12px', display: 'flex', alignItems: 'center', gap: '6px' }}
          >
            {theme === 'dark' ? <Sun size={18} color="#fbbf24" /> : <Moon size={18} color="#8b5cf6" />}
            <span style={{ fontSize: '0.8rem', fontWeight: '600' }}>
              {theme === 'dark' ? 'Light' : 'Dark'} Mode
            </span>
          </button>

          {/* User Auth Profile Status */}
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-main)', display: 'block' }}>
                  {user.name}
                </span>
                <span className="badge badge-info" style={{ fontSize: '0.68rem', padding: '2px 6px' }}>
                  {user.role}
                </span>
              </div>
              <button 
                className="btn-secondary" 
                onClick={handleLogout} 
                title="Sign Out"
                style={{ padding: '8px', color: '#ef4444' }}
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <button 
              className="btn-primary" 
              onClick={() => setIsAuthOpen(true)}
              style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <LogIn size={16} /> Sign In / Register
            </button>
          )}

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
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
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

      {/* Auth Modal */}
      <AuthModal 
        isOpen={isAuthOpen} 
        onClose={() => setIsAuthOpen(false)} 
        onAuthSuccess={handleAuthSuccess} 
      />

      {/* Footer */}
      <footer style={{ textAlign: 'center', marginTop: '40px', padding: '20px', color: 'var(--text-sub)', fontSize: '0.8rem', borderTop: '1px solid var(--border-color)' }}>
        DarkTrust – Zero Trust Access Control for Decentralized APIs | Developed for InnovaHack Hackathon 2026
      </footer>

    </div>
  );
}
