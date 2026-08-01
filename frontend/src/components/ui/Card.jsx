import React from 'react';
import PropTypes from 'prop-types';

/**
 * Card component with optional header and footer.
 * Props:
 *  - title: string (optional header text)
 *  - children: node – main content
 *  - footer: node (optional footer)
 *  - hover: boolean – adds subtle elevation on hover
 */
export default function Card({ title, children, footer, hover = true }) {
  const base = 'bg-surface-800 text-surface-100 rounded-lg shadow-sm p-4';
  const hoverClass = hover ? 'hover:shadow-md transition-shadow' : '';
  return (
    <div className={`${base} ${hoverClass}`}>
      {title && <h3 className="text-lg font-display mb-2 text-white">{title}</h3>}
      <div className="mb-2">{children}</div>
      {footer && <div className="border-t border-surface-700 pt-2 mt-2 text-sm text-surface-300">{footer}</div>}
    </div>
  );
}

Card.propTypes = {
  title: PropTypes.string,
  children: PropTypes.node.isRequired,
  footer: PropTypes.node,
  hover: PropTypes.bool,
};
