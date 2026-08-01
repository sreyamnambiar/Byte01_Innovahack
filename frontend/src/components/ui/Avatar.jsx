import React from 'react';
import PropTypes from 'prop-types';

/**
 * Avatar component – displays a user image or initials.
 * Props:
 *  - src: image URL (optional)
 *  - alt: alt text for the image
 *  - initials: string – shown when `src` is missing
 *  - size: 'sm' | 'md' | 'lg' (default 'md')
 */
export default function Avatar({ src, alt = 'avatar', initials = '', size = 'md' }) {
  const sizeClasses = {
    sm: 'h-8 w-8 text-sm',
    md: 'h-10 w-10 text-base',
    lg: 'h-12 w-12 text-lg',
  }[size];

  const base = `flex-shrink-0 rounded-full bg-surface-700 text-surface-100 flex items-center justify-center ${sizeClasses}`;

  return src ? (
    <img src={src} alt={alt} className={`${base} object-cover`} />
  ) : (
    <div className={base}>{initials}</div>
  );
}

Avatar.propTypes = {
  src: PropTypes.string,
  alt: PropTypes.string,
  initials: PropTypes.string,
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
};
