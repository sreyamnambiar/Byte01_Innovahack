import { NavLink } from 'react-router-dom';
import { useState } from 'react';
import { XMarkIcon, Bars3Icon } from '@heroicons/react/24/solid';

/**
 * Sidebar navigation component.
 * Receives an array of navigation items:
 * [{ label, to, icon: Component }]
 * Uses Tailwind dark theme and collapses on small screens.
 */
export default function Sidebar({ items = [] }) {
  const [open, setOpen] = useState(true);
  return (
    <aside className={`bg-surface-800 text-surface-100 transition-width duration-300 ${open ? 'w-64' : 'w-16'} h-screen flex flex-col`}> 
      <div className="flex items-center justify-between px-4 py-3">
        {open && <span className="font-display text-lg">Menu</span>}
        <button onClick={() => setOpen(!open)} className="p-1 rounded hover:bg-surface-700">
          {open ? <XMarkIcon className="h-5 w-5" /> : <Bars3Icon className="h-5 w-5" />}
        </button>
      </div>
      <nav className="flex-1 overflow-y-auto">
        {items.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-2 rounded transition-colors ${isActive ? 'bg-primary-600 text-white' : 'hover:bg-surface-700'} `
            }
          >
            {item.icon && <item.icon className="h-5 w-5" />}
            {open && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
