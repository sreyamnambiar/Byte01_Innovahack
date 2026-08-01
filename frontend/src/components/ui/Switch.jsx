import React from 'react';
import PropTypes from 'prop-types';

/**
 * Switch (toggle) component.
 * Props:
 *   - checked: boolean – controlled state
 *   - onChange: function(event) – called with new checked value
 *   - disabled: boolean
 *   - size: 'sm' | 'md' | 'lg' (default 'md')
 */
export default function Switch({ checked = false, onChange, disabled = false, size = 'md' }) {
  const sizeClasses = {
    sm: 'h-4 w-7 after:h-3 after:w-3',
    md: 'h-5 w-9 after:h-4 after:w-4',
    lg: 'h-6 w-11 after:h-5 after:w-5',
  }[size];

  return (
    <label className="inline-flex items-center cursor-pointer">
      <input
        type="checkbox"
        className="sr-only"
        checked={checked}
        onChange={e => onChange && onChange(e.target.checked)}
        disabled={disabled}
      />
      <div
        className={`relative ${sizeClasses} rounded-full transition-colors ${disabled ? 'opacity-40 cursor-not-allowed' : ''} ${checked ? 'bg-primary-600' : 'bg-surface-600'}`}
      >
        <span
          className={`absolute left-0 top-0 bottom-0 m-0.5 bg-surface-900 rounded-full transition-transform ${checked ? 'translate-x-full' : ''}`}
        />
      </div>
    </label>
  );
}

Switch.propTypes = {
  checked: PropTypes.bool,
  onChange: PropTypes.func,
  disabled: PropTypes.bool,
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
};
