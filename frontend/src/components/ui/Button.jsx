import React from 'react';
import Loader from '@/components/ui/Loader';


/**
 * Reusable button component.
 * Props:
 *  - variant: 'primary' | 'secondary' | 'outline' (default: 'primary')
 *  - size: 'sm' | 'md' | 'lg' (default: 'md')
 *  - loading: boolean – shows spinner and disables button
 *  - disabled: boolean – disables button
 *  - onClick: function
 *  - children: node
 * Uses Tailwind dark‑theme classes.
 */
export default function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  onClick,
  children,
  ...rest
}) {
  const base = 'rounded transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-5 py-3 text-lg',
  }[size];

  const variants = {
    primary: `bg-primary-600 hover:bg-primary-500 text-white ${base}`,
    secondary: `bg-surface-700 hover:bg-surface-600 text-surface-100 ${base}`,
    outline: `border border-primary-500 text-primary-500 hover:bg-primary-500/10 ${base}`,
  }[variant];

  const isDisabled = loading || disabled;

  return (
    <button
      type="button"
      className={`${sizes} ${variants} ${isDisabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      onClick={onClick}
      disabled={isDisabled}
      {...rest}
    >
      {loading ? <Spinner size="sm" className="mr-2" /> : null}
      {children}
    </button>
  );
}

Button.propTypes = {
  variant: PropTypes.oneOf(['primary', 'secondary', 'outline']),
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  loading: PropTypes.bool,
  disabled: PropTypes.bool,
  onClick: PropTypes.func,
  children: PropTypes.node.isRequired,
};
