import React from 'react';
/**
 * Simple statistic card used on the dashboard.
 * Props: title, value, color (Tailwind color prefix).
 */
export default function StatCard({ title, value, color = 'primary' }) {
  return (
    <div className={`bg-${color}-800/30 border border-${color}-500/30 backdrop-blur-sm rounded-xl p-4 text-${color}-100`}> 
      <p className="text-sm opacity-80">{title}</p>
      <p className="text-2xl font-semibold mt-1">{value}</p>
    </div>
  );
}
