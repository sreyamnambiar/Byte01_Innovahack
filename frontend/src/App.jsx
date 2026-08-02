import React, { useState, useEffect } from 'react';
import { Shield, Zap, Sliders, Activity, Play, Terminal, Lock, Sun, Moon, LogIn, LogOut, LayoutDashboard, Home } from 'lucide-react';
import MetricsOverview from './components/MetricsOverview';
import ServiceMeshVisualizer from './components/ServiceMeshVisualizer';
import AttackSimulator from './components/AttackSimulator';
import PolicyManager from './components/PolicyManager';
import ProxyTester from './components/ProxyTester';
import AuditLogFeed from './components/AuditLogFeed';
import AuthModal from './components/AuthModal';
import LandingPage from './components/LandingPage';

export default function App() {
  const [view, setView] = useState('landing'); // 'landing' or 'dashboard'
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
    setView('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    setToken('');
    localStorage.removeItem('darktrust-user');
    localStorage.removeItem('darktrust-token');
    setView('landing');
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
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px 16px' }}>
      
      {/* Top Header Bar */}
      <header className="glass-panel" style={{ padding: '16px 24px', marginBottom: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        
        {/* Logo & Title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px', cursor: 'pointer' }} onClick={() => setView('landing')}>
          <div style={{ background: '#ffffff', padding: '4px', borderRadius: '10px', boxShadow: '0 0 14px var(--primary-glow)', border: '1px solid var(--primary-cyan)', display: 'inline-flex' }}>
            <img 
              src="/logo.png" 
              alt="DarkTrust Logo" 
              style={{ width: '38px', height: '38px', objectFit: 'contain' }} 
            />
          </div>
          <div>
            <h1 style={{ fontSize: '1.3rem', fontWeight: '800', letterSpacing: '-0.02em', color: 'var(--text-main)' }}>
              Dark<span style={{ color: 'var(--primary-cyan)' }}>Trust</span> Security
            </h1>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Zero-Trust Access Control for Decentralized APIs
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          
          {/* View Switcher */}
          <button 
            className={view === 'landing' ? 'btn-primary' : 'btn-secondary'}
            onClick={() => setView('landing')}
            style={{ padding: '8px 12px', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}
          >
            <Home size={16} /> Overview Pitch
          </button>

          <button 
            className={view === 'dashboard' ? 'btn-primary' : 'btn-secondary'}
            onClick={() => setView('dashboard')}
            style={{ padding: '8px 12px', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}
          >
            <LayoutDashboard size={16} /> Security Dashboard
          </button>

          {/* Light / Dark Mode Toggle */}
          <button 
            className="btn-secondary" 
            onClick={toggleTheme}
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
            style={{ padding: '8px 12px', display: 'flex', alignItems: 'center', gap: '6px' }}
          >
            {theme === 'dark' ? <Sun size={18} color="#fbbf24" /> : <Moon size={18} color="#8b5cf6" />}
            <span style={{ fontSize: '0.8rem', fontWeight: '600' }}>
              {theme === 'dark' ? 'Light' : 'Dark'}
            </span>
          </button>

          {/* User Session Profile */}
          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ textAlign: 'right' }}>
                <span style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-main)', display: 'block' }}>
                  {user.name}
                </span>
                <span className="badge badge-info" style={{ fontSize: '0.65rem', padding: '2px 6px' }}>
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
              style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}
            >
              <LogIn size={16} /> Sign In
            </button>
          )}

        </div>
      </header>

      {/* RENDER VIEW: LANDING PAGE vs DASHBOARD */}
      {view === 'landing' ? (
        <LandingPage 
          onAuthSuccess={handleAuthSuccess}
          onExploreDemo={() => setView('dashboard')}
        />
      ) : (
        <>
          {/* Dashboard Telemetry Overview */}
          <MetricsOverview metrics={metrics} />

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

          {/* Active Tab Content */}
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
        </>
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
