import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { createPortal } from 'react-dom';

/**
 * Modal component with backdrop.
 * Props:
 *  - isOpen: boolean – controls visibility
 *  - onClose: function – called when backdrop or close button is clicked
 *  - title: string (optional header)
 *  - children: modal body content
 *  - size: 'sm' | 'md' | 'lg' (default 'md')
 */
export default function Modal({ isOpen, onClose, title, children, size = 'md' }) {
  // Prevent body scroll when modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
  }[size];

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className={`bg-surface-800 text-surface-100 rounded-lg shadow-xl p-6 w-full ${sizeClasses}`}> 
        <div className="flex justify-between items-center mb-4">
          {title && <h2 className="text-lg font-display text-white">{title}</h2>}
          <button
            onClick={onClose}
            className="text-surface-300 hover:text-white transition-colors"
            aria-label="Close modal"
          >
            ✕
          </button>
        </div>
        <div className="overflow-y-auto max-h-[70vh]">{children}</div>
      </div>
    </div>,
    document.body
  );
}

Modal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  title: PropTypes.string,
  children: PropTypes.node.isRequired,
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
};
