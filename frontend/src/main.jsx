/**
 * DarkTrust – React Application Entry Point
 *
 * Mounts the root React component into the DOM.
 * Strict Mode is enabled to surface potential issues during development.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';

import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
