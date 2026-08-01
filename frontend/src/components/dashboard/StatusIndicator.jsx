import React from 'react';
/**
 * StatusIndicator – placeholder component to show overall system status.
 * Props: optional `status` string (e.g., 'healthy', 'degraded', 'down').
 */
export default function StatusIndicator({ status = 'healthy' }) {
  const colorMap = {
    healthy: 'bg-success-600',
    degraded: 'bg-warning-600',
    down: 'bg-danger-600',
  }[status] || 'bg-surface-600';

  const labelMap = {
    healthy: 'All systems operational',
    degraded: 'Some issues detected',
    down: 'System down',
  }[status] || 'Status unknown';

  return (
    <div className={`flex items-center space-x-2 p-3 rounded bg-surface-800/30 backdrop-blur-sm border ${colorMap}`}>
      <span className="w-3 h-3 rounded-full bg-current" />
      <span className="text-sm font-medium text-surface-100">{labelMap}</span>
    </div>
  );
}
