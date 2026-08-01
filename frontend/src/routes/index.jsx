/**
 * DarkTrust – Centralized Route Definitions
 *
 * All application routes are defined here.
 * This is the single source of truth for routing.
 *
 * Route Organization:
 * - Public routes:     Accessible without authentication
 * - Protected routes:  Require valid JWT + trust evaluation
 * - Admin routes:      Require admin role + elevated trust score
 *
 * As pages and layouts are developed, import and register them below.
 * The ProtectedRoute and RoleGuard wrappers will be added with the auth module.
 */

import { Routes, Route } from 'react-router-dom';

/**
 * Route path constants.
 * Using constants prevents typos and enables programmatic navigation.
 *
 * Usage:
 *   import { ROUTES } from '@/routes';
 *   navigate(ROUTES.DASHBOARD);
 */
export const ROUTES = {
  // Public
  HOME:       '/',
  LOGIN:      '/login',
  REGISTER:   '/register',
  FORBIDDEN:  '/403',
  NOT_FOUND:  '/404',

  // Protected – Platform
  DASHBOARD:   '/dashboard',
  POLICIES:    '/policies',
  GATEWAY:     '/gateway',
  AUDIT_LOGS:  '/audit',
  RISK_SCORES: '/risk',

  // Admin
  ADMIN:       '/admin',
  ADMIN_USERS: '/admin/users',
};

/**
 * AppRoutes component.
 *
 * Renders the React Router route tree.
 * Page components will be imported and added here as modules are developed.
 *
 * Pattern:
 *   <Route element={<MainLayout />}>
 *     <Route path={ROUTES.DASHBOARD} element={<DashboardPage />} />
 *   </Route>
 */
function AppRoutes() {
  return (
    <Routes>
      {/*
       * ── Temporary placeholder route ────────────────────────────────
       * This will be replaced with actual page components in future modules.
       * The inline component below is ONLY a foundation placeholder.
       */}
      <Route
        path="*"
        element={
          <div className="min-h-screen bg-surface-900 flex items-center justify-center">
            <div className="text-center animate-fade-in-up">
              <div className="text-primary-500 font-mono text-sm mb-4 tracking-widest uppercase">
                DarkTrust Platform
              </div>
              <h1 className="text-4xl font-display font-bold text-white mb-3">
                Foundation Ready
              </h1>
              <p className="text-surface-400 text-lg mb-8 max-w-md">
                The project scaffold is configured. Pages will be added module by module.
              </p>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-sm font-mono">
                <span className="w-2 h-2 rounded-full bg-primary-500 animate-pulse-slow" />
                Zero Trust Engine: Initializing
              </div>
            </div>
          </div>
        }
      />
    </Routes>
  );
}

export default AppRoutes;
