import React, { useState } from 'react';
import { Server, Database, ShieldAlert, CheckCircle, ShieldX, RefreshCw } from 'lucide-react';

export default function ServiceMeshVisualizer({ lastEvent }) {
  const [selectedNode, setSelectedNode] = useState(null);

  const nodes = [
    { id: 'client', name: 'External Client', type: 'user', x: 80, y: 150, port: 'Browser/Mobile' },
    { id: 'edge-gateway', name: 'Edge Gateway', type: 'gateway', x: 260, y: 150, port: '8080' },
    { id: 'auth-service', name: 'Auth Service', type: 'service', x: 460, y: 70, port: '8001' },
    { id: 'user-service', name: 'User Microservice', type: 'service', x: 460, y: 230, port: '8002' },
    { id: 'analytics-service', name: 'Analytics Service', type: 'service', x: 660, y: 70, port: '8003' },
    { id: 'database-api', name: 'Backend Database API', type: 'db', x: 720, y: 230, port: '5432' },
  ];

  // Active status based on last event
  const isBreachActive = lastEvent && lastEvent.status === "BLOCKED";
  const breachCaller = lastEvent?.caller;
  const breachTarget = lastEvent?.target;

  return (
    <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: 'var(--text-main)' }}>
            🕸️ Dynamic Service Mesh Topology & Threat Monitor
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '2px' }}>
            Real-time microservice communication mesh with zero-trust proxy interceptor points.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <span className="badge badge-success">
            <CheckCircle size={12} /> Cryptographic Mesh Active
          </span>
          {isBreachActive && (
            <span className="badge badge-danger">
              <ShieldAlert size={12} /> Lateral Breach Intercepted
            </span>
          )}
        </div>
      </div>

      {/* SVG Canvas Mesh Diagram */}
      <div style={{ background: '#05070a', borderRadius: '12px', border: '1px solid var(--border-color)', position: 'relative', overflow: 'hidden' }}>
        <svg width="100%" height="320" viewBox="0 0 850 300" style={{ display: 'block' }}>
          <defs>
            <linearGradient id="legitGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#00f0ff" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#10b981" stopOpacity="0.8" />
            </linearGradient>
            <linearGradient id="breachGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#ef4444" stopOpacity="1" />
              <stop offset="100%" stopColor="#ff0055" stopOpacity="1" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          {/* Topology Connection Lines */}
          {/* Client -> Edge */}
          <path d="M 120 150 L 220 150" stroke="url(#legitGrad)" strokeWidth="3" filter="url(#glow)" />
          
          {/* Edge -> Auth */}
          <path d="M 300 130 L 420 85" stroke="url(#legitGrad)" strokeWidth="2.5" strokeDasharray="6,4" />
          
          {/* Edge -> User */}
          <path d="M 300 170 L 420 215" stroke="url(#legitGrad)" strokeWidth="2.5" strokeDasharray="6,4" />

          {/* User -> DB */}
          <path d="M 500 230 L 680 230" stroke="url(#legitGrad)" strokeWidth="3" filter="url(#glow)" />

          {/* Analytics -> DB */}
          <path d="M 500 70 L 680 215" stroke="url(#legitGrad)" strokeWidth="2" strokeDasharray="4,4" />

          {/* LATERAL MOVEMENT ATTACK PATH (Edge -> DB direct hop attempt) */}
          <path d="M 300 150 Q 510 290 680 230" 
                stroke={isBreachActive && breachCaller === 'edge-gateway' && breachTarget === 'database-api' ? "url(#breachGrad)" : "rgba(239, 68, 68, 0.25)"} 
                strokeWidth={isBreachActive ? "4" : "1.5"} 
                strokeDasharray="8,4" 
                filter={isBreachActive ? "url(#glow)" : "none"} />

          {/* Interceptor Shield Icon on Lateral Path */}
          <circle cx="510" cy="245" r="16" fill="#ef4444" opacity="0.9" filter="url(#glow)" />
          <text x="510" y="249" fill="white" fontSize="11" textAnchor="middle" fontWeight="bold">🛡️</text>

          {/* Render Nodes */}
          {nodes.map((node) => {
            const isSelected = selectedNode?.id === node.id;
            const isTargeted = breachTarget === node.id || breachCaller === node.id;

            return (
              <g key={node.id} 
                 transform={`translate(${node.x}, ${node.y})`} 
                 onClick={() => setSelectedNode(node)}
                 style={{ cursor: 'pointer' }}>
                <rect x="-45" y="-28" width="90" height="56" rx="10" 
                      fill={isTargeted && isBreachActive ? "rgba(239, 68, 68, 0.2)" : isSelected ? "rgba(0, 240, 255, 0.2)" : "#0f172a"} 
                      stroke={isTargeted && isBreachActive ? "#ef4444" : isSelected ? "#00f0ff" : "rgba(255, 255, 255, 0.15)"} 
                      strokeWidth={isSelected || isTargeted ? "2.5" : "1.5"} 
                      filter={isSelected || isTargeted ? "url(#glow)" : "none"} />
                
                <text x="0" y="-8" fill="#ffffff" fontSize="11" fontWeight="700" textAnchor="middle">
                  {node.name.split(' ')[0]}
                </text>
                <text x="0" y="8" fill="var(--text-muted)" fontSize="9" textAnchor="middle">
                  {node.name.split(' ').slice(1).join(' ')}
                </text>
                <text x="0" y="20" fill="var(--primary-cyan)" fontSize="8" fontFamily="monospace" textAnchor="middle">
                  Port: {node.port}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Legend & Selected Node Telemetry */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '16px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
        <div style={{ display: 'flex', gap: '20px' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ width: '12px', height: '3px', background: '#00f0ff', borderRadius: '2px', display: 'inline-block' }}></span> Authorized Hop
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ width: '12px', height: '3px', background: '#ef4444', borderRadius: '2px', display: 'inline-block' }}></span> Blocked Lateral Hop
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span>🛡️</span> Zero-Trust Proxy Interceptor
          </span>
        </div>

        {selectedNode ? (
          <div style={{ color: 'var(--primary-cyan)', fontWeight: '600' }}>
            Selected: {selectedNode.name} ({selectedNode.id})
          </div>
        ) : (
          <div>Click node to inspect microservice telemetry</div>
        )}
      </div>
    </div>
  );
}
