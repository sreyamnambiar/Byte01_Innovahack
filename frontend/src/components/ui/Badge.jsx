import React from 'react';
import PropTypes from 'prop-types';

/**
 * Badge component for tags, status labels, etc.
 * Props:
 *  - variant: 'primary' | 'secondary' | 'success' | 'warning' | 'danger'
 *  - children: node – label text
 * Uses Tailwind colors defined in the dark theme.
 */
export default function Badge({ variant = 'primary', children }) {
  const base = 'px-2 py-0.5 rounded-full text-xs font-medium';
  const colors = {
    primary: 'bg-primary-600 text-primary-100',
    secondary: 'bg-surface-600 text-surface-100',
    success: 'bg-success-500 text-white',
    warning: 'bg-warning-500 text-white',
    danger: 'bg-danger-500 text-white',
  }[variant];
  return <span className={`${base} ${colors}`}>{children}</span>;
}

Badge.propTypes = {
  variant: PropTypes.oneOf(['primary', 'secondary', 'success', 'warning', 'danger']),
  children: PropTypes.node.isRequired,
};
