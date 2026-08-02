import React, { useState } from 'react';
import { X, LogIn, UserPlus, ShieldCheck, Key, Lock, Mail, User } from 'lucide-react';

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('edge-gateway');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
    const body = isLogin 
      ? { email, password } 
      : { email, password, name, role };

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || 'Authentication failed');
      }

      if (isLogin) {
        onAuthSuccess(data.user, data.access_token);
        onClose();
      } else {
        const loginRes = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const loginData = await loginRes.json();
        onAuthSuccess(loginData.user, loginData.access_token);
        onClose();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = (demoEmail, demoPassword) => {
    setEmail(demoEmail);
    setPassword(demoPassword);
    setIsLogin(true);
  };

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0, 0, 0, 0.75)', backdropFilter: 'blur(8px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      
      <div className="glass-panel" style={{ width: '100%', maxWidth: '440px', padding: '28px', position: 'relative' }}>
        
        <button 
          onClick={onClose}
          style={{ position: 'absolute', top: '16px', right: '16px', background: 'transparent', color: 'var(--text-muted)' }}
        >
          <X size={20} />
        </button>

        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <img 
            src="/logo.png" 
            alt="DarkTrust Logo" 
            style={{ width: '56px', height: '56px', borderRadius: '12px', objectFit: 'cover', border: '1px solid var(--border-accent)', marginBottom: '8px' }} 
          />
          <h3 style={{ fontSize: '1.3rem', fontWeight: '800', color: 'var(--text-main)' }}>
            {isLogin ? 'Sign In to DarkTrust' : 'Create DarkTrust Account'}
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Zero-Trust Access Control & Identity Verification
          </p>
        </div>

        {/* Tab Switcher */}
        <div style={{ display: 'flex', background: 'var(--input-bg)', borderRadius: '8px', padding: '4px', marginBottom: '20px', border: '1px solid var(--border-color)' }}>
          <button 
            style={{ flex: 1, padding: '8px', borderRadius: '6px', fontSize: '0.85rem', fontWeight: '600', background: isLogin ? 'var(--bg-card-hover)' : 'transparent', color: isLogin ? 'var(--primary-cyan)' : 'var(--text-muted)' }}
            onClick={() => setIsLogin(true)}
          >
            Sign In
          </button>
          <button 
            style={{ flex: 1, padding: '8px', borderRadius: '6px', fontSize: '0.85rem', fontWeight: '600', background: !isLogin ? 'var(--bg-card-hover)' : 'transparent', color: !isLogin ? 'var(--primary-cyan)' : 'var(--text-muted)' }}
            onClick={() => setIsLogin(false)}
          >
            Create Account
          </button>
        </div>

        {error && (
          <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', color: '#ef4444', padding: '10px', borderRadius: '6px', fontSize: '0.8rem', marginBottom: '16px' }}>
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          
          {!isLogin && (
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Full Name</label>
              <div style={{ position: 'relative' }}>
                <User size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--text-sub)' }} />
                <input 
                  type="text"
                  required
                  placeholder="Security Officer"
                  style={{ width: '100%', padding: '10px 10px 10px 36px', background: 'var(--input-bg)', border: '1px solid var(--border-color)', color: 'var(--text-main)', borderRadius: '6px' }}
                  value={name}
                  onChange={e => setName(e.target.value)}
                />
              </div>
            </div>
          )}

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Email Address</label>
            <div style={{ position: 'relative' }}>
              <Mail size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--text-sub)' }} />
              <input 
                type="email"
                required
                placeholder="admin@darktrust.io"
                style={{ width: '100%', padding: '10px 10px 10px 36px', background: 'var(--input-bg)', border: '1px solid var(--border-color)', color: 'var(--text-main)', borderRadius: '6px' }}
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Password</label>
            <div style={{ position: 'relative' }}>
              <Lock size={16} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--text-sub)' }} />
              <input 
                type="password"
                required
                placeholder="••••••••"
                style={{ width: '100%', padding: '10px 10px 10px 36px', background: 'var(--input-bg)', border: '1px solid var(--border-color)', color: 'var(--text-main)', borderRadius: '6px' }}
                value={password}
                onChange={e => setPassword(e.target.value)}
              />
            </div>
          </div>

          {!isLogin && (
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Assign Microservice Role</label>
              <select 
                style={{ width: '100%', padding: '10px', background: 'var(--input-bg)', border: '1px solid var(--border-color)', color: 'var(--text-main)', borderRadius: '6px' }}
                value={role}
                onChange={e => setRole(e.target.value)}
              >
                <option value="admin">Security Admin (Full Access)</option>
                <option value="edge-gateway">edge-gateway</option>
                <option value="user-service">user-service</option>
              </select>
            </div>
          )}

          <button className="btn-primary" type="submit" disabled={loading} style={{ marginTop: '8px', padding: '12px' }}>
            {loading ? 'Processing...' : isLogin ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        {/* Demo Login Shortcuts */}
        <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--border-color)' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-sub)', display: 'block', marginBottom: '8px', textAlign: 'center' }}>
            ⚡ QUICK DEMO LOGINS
          </span>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button 
              className="btn-secondary" 
              style={{ flex: 1, fontSize: '0.75rem', padding: '6px' }}
              onClick={() => handleQuickDemo('admin@darktrust.io', 'admin123')}
            >
              🔑 Login Admin
            </button>
            <button 
              className="btn-secondary" 
              style={{ flex: 1, fontSize: '0.75rem', padding: '6px' }}
              onClick={() => handleQuickDemo('engineer@darktrust.io', 'engineer123')}
            >
              👤 Login Engineer
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
