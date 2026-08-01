import React from 'react';

/**
 * Header component for the MainLayout.
 * Displays the application title and a theme toggle (placeholder).
 */
export default function Header() {
  return (
    <header className="flex items-center justify-between px-4 py-3 bg-surface-800 border-b border-surface-700">
      <h1 className="text-xl font-display text-white">Zero Trust Access Control</h1>
      {/* Placeholder for future theme toggle or user menu */}
      <button className="text-surface-300 hover:text-white transition-colors">
        <span className="sr-only">Toggle theme</span>
        🌙
      </button>
    </header>
  );
}
