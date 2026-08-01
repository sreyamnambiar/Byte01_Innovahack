import React from 'react';
import PropTypes from 'prop-types';

/**
 * Reusable input component with optional label.
 * Props:
 *  - id (required), name, type (default 'text'), placeholder, label
 *  - disabled, readOnly, className for custom styling
 */
export default function Input({ id, name, type = 'text', placeholder, label, disabled, readOnly, className = '', ...rest }) {
  const inputClass = `bg-surface-700 text-surface-100 placeholder-surface-400 border border-surface-600 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition ${className}`;
  const inputElement = (
    <input
      id={id}
      name={name}
      type={type}
      placeholder={placeholder}
      disabled={disabled}
      readOnly={readOnly}
      className={inputClass}
      {...rest}
    />
  );
  return label ? (
    <label className="block text-sm font-medium text-surface-200 mb-1" htmlFor={id}>
      {label}
      {inputElement}
    </label>
  ) : (
    inputElement
  );
}

Input.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string,
  type: PropTypes.string,
  placeholder: PropTypes.string,
  label: PropTypes.string,
  disabled: PropTypes.bool,
  readOnly: PropTypes.bool,
  className: PropTypes.string,
};
