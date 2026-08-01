import React from 'react';
import PropTypes from 'prop-types';

/**
 * Tooltip component – shows a hover tooltip.
 * Props:
 *  - content: tooltip text
 *  - children: the element that triggers the tooltip
 *  - position: 'top' | 'right' | 'bottom' | 'left' (default 'top')
 */
export default function Tooltip({ content, children, position = 'top' }) {
  const positionClasses = {
    top: 'bottom-full mb-2 left-1/2 -translate-x-1/2',
    bottom: 'top-full mt-2 left-1/2 -translate-x-1/2',
    left: 'right-full mr-2 top-1/2 -translate-y-1/2',
    right: 'left-full ml-2 top-1/2 -translate-y-1/2',
  }[position];

  return (
    <div className="relative inline-block">
      {children}
      <div className={`absolute ${positionClasses} whitespace-nowrap rounded bg-surface-800 text-surface-100 text-xs px-2 py-1 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity`}>
        {content}
      </div>
    </div>
  );
}

Tooltip.propTypes = {
  content: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  position: PropTypes.oneOf(['top', 'right', 'bottom', 'left']),
};
