import React from 'react';
import PropTypes from 'prop-types';

/**
 * Small colored dot indicating a status.
 * Props:
 *  - variant: 'success' | 'warning' | 'danger' | 'info' (default 'info')
 *  - size: 'xs' | 'sm' | 'md' (default 'sm')
 */
export default function StatusDot({ variant = 'info', size = 'sm' }) {
  const sizeMap = {
    xs: 'h-2 w-2',
    sm: 'h-3 w-3',
    md: 'h-4 w-4',
  }[size];
  const colorMap = {
    success: 'bg-success-500',
    warning: 'bg-warning-500',
    danger: 'bg-danger-500',
    info: 'bg-primary-500',
  }[variant];
  return <span className={`inline-block rounded-full ${sizeMap} ${colorMap}`} />;
}

StatusDot.propTypes = {
  variant: PropTypes.oneOf(['success', 'warning', 'danger', 'info']),
  size: PropTypes.oneOf(['xs', 'sm', 'md']),
};
