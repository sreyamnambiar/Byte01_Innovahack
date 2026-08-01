import React from 'react';
import { Card } from '@/components/ui'; // generic Card if needed
import StatCard from '@/components/dashboard/StatCard';
import DataTable from '@/components/dashboard/DataTable';
import StatusIndicator from '@/components/dashboard/StatusIndicator';
import LineChart from '@/components/chart/LineChart';
import BarChart from '@/components/chart/BarChart';
import DonutChart from '@/components/chart/DonutChart';

/**
 * Security Dashboard – mock data version.
 * Demonstrates layout, stat cards, charts, and a table.
 * All styling follows the dark‑enterprise theme (surface‑800, primary‑600, glow‑primary).
 */
export default function Dashboard() {
  // Mock data
  const stats = [
    { title: 'Total APIs', value: 42, color: 'primary' },
    { title: 'Active Policies', value: 12, color: 'secondary' },
    { title: 'Risk Score', value: '7.3', color: 'danger' },
    { title: 'Security Alerts', value: 5, color: 'warning' },
  ];

  const recentActivities = [
    { id: 1, api: 'User Service', action: 'Policy Updated', time: '2m ago' },
    { id: 2, api: 'Payment API', action: 'Alert Triggered', time: '10m ago' },
    { id: 3, api: 'Auth Service', action: 'New API Added', time: '30m ago' },
  ];

  return (
    <div className="p-6 space-y-6 bg-surface-900 min-h-screen text-surface-100">
      {/* 1. Summary statistics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s) => (
          <StatCard
            key={s.title}
            title={s.title}
            value={s.value}
            color={s.color}
          />
        ))}
      </div>

      {/* 2. Analytics charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="bg-surface-800/30 backdrop-blur-sm border border-primary-500/30">
          <h2 className="text-lg font-medium mb-2 text-primary-600">Risk Trend</h2>
          <LineChart data={[]} />
        </Card>
        <Card className="bg-surface-800/30 backdrop-blur-sm border border-primary-500/30">
          <h2 className="text-lg font-medium mb-2 text-primary-600">API Activity</h2>
          <BarChart data={[]} />
        </Card>
        <Card className="bg-surface-800/30 backdrop-blur-sm border border-primary-500/30 col-span-2">
          <h2 className="text-lg font-medium mb-2 text-primary-600">Threat Distribution</h2>
          <DonutChart data={[]} />
        </Card>
      </div>

      {/* 3. Recent activity table */}
      <Card className="bg-surface-800/30 backdrop-blur-sm border border-primary-500/30">
        <h2 className="text-lg font-medium mb-2 text-primary-600">Recent Activity</h2>
        <DataTable data={recentActivities} />
      </Card>

      {/* 4. API health monitoring placeholder */}
      <Card className="bg-surface-800/30 backdrop-blur-sm border border-primary-500/30">
        <h2 className="text-lg font-medium mb-2 text-primary-600">API Health Monitoring</h2>
        <p className="text-sm opacity-80">(Mock view – health stats will appear here)</p>
      </Card>
    </div>
  );
}
