/**
 * DarkTrust – Axios API Service
 *
 * Configures a base Axios instance for all HTTP communication
 * with the DarkTrust FastAPI backend.
 *
 * Features:
 * - Base URL from environment variables
 * - Default request/response headers
 * - Request interceptor: Attach JWT token to Authorization header
 * - Response interceptor: Handle 401 (token expiry) globally
 *
 * Usage:
 *   import api from '@/services/api';
 *   const { data } = await api.get('/api/v1/health');
 */

import axios from 'axios';

// ── Constants ─────────────────────────────────────────────────────────────
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT  = 30_000; // 30 seconds

// ── Axios Instance ────────────────────────────────────────────────────────
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept':       'application/json',
    'X-Client':     'DarkTrust-Frontend/1.0',
  },
});

// ── Request Interceptor ────────────────────────────────────────────────────
/**
 * Attach the JWT Bearer token to every outgoing request.
 * The token is retrieved from localStorage (pattern will be refined
 * when the AuthContext and token management module is added).
 */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('darktrust_access_token');

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    // Attach a unique request ID for distributed tracing (future)
    config.headers['X-Request-ID'] = crypto.randomUUID();

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// ── Response Interceptor ──────────────────────────────────────────────────
/**
 * Handle common HTTP error states globally:
 * - 401 Unauthorized: Clear tokens, redirect to login
 * - 403 Forbidden:    Redirect to access denied page
 * - 500+ Server:      Log and pass through for UI handling
 */
api.interceptors.response.use(
  (response) => {
    // Successful responses pass through unchanged
    return response;
  },
  (error) => {
    const status = error?.response?.status;

    if (status === 401) {
      // Token expired or invalid — clear storage and force re-login
      // Navigation logic will be wired to AuthContext in the auth module
      localStorage.removeItem('darktrust_access_token');
      localStorage.removeItem('darktrust_refresh_token');

      // TODO: Dispatch logout action to AuthContext
      // TODO: Navigate to ROUTES.LOGIN
    }

    if (status === 403) {
      // Access denied — will navigate to 403 page via router
      // TODO: Navigate to ROUTES.FORBIDDEN
    }

    return Promise.reject(error);
  },
);

export default api;
