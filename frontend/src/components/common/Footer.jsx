import React from 'react';

/**
 * Footer component used in MainLayout.
 * Simple dark footer with branding.
 */
export default function Footer() {
  return (
    <footer className="bg-surface-800 text-surface-200 py-3 text-center text-sm">
      © {new Date().getFullYear()} Zero Trust Access Control – All rights reserved.
    </footer>
  );
}
