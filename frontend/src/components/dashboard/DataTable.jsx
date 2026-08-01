import React from 'react';
/**
 * Simple data table component for the dashboard.
 * Props:
 *   - data: array of objects with consistent keys
 */
export default function DataTable({ data = [] }) {
  if (data.length === 0) {
    return <p className="text-sm opacity-80">No data available.</p>;
  }
  const headers = Object.keys(data[0]);
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm text-left text-surface-200">
        <thead className="bg-surface-800">
          <tr>
            {headers.map((h) => (
              <th key={h} className="px-4 py-2 font-medium uppercase">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-surface-700">
          {data.map((row, idx) => (
            <tr key={idx} className="hover:bg-surface-800/30">
              {headers.map((h) => (
                <td key={h} className="px-4 py-2">
                  {row[h]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
