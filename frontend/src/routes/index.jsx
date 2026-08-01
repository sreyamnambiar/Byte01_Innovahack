import { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from '@/layouts/MainLayout';

// Lazy‑load page components for code‑splitting
const Dashboard = lazy(() => import('@/pages/Dashboard'));
const Apis = lazy(() => import('@/pages/Apis'));
const PolicyEditor = lazy(() => import('@/pages/PolicyEditor'));
const Settings = lazy(() => import('@/pages/Settings'));

function AppRoutes() {
  return (
    <Suspense fallback={null}>
      <Routes>
        <Route element={<MainLayout />}> 
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/apis" element={<Apis />} />
          <Route path="/policies" element={<PolicyEditor />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
        {/* TODO: Add a fallback 404 page */}
      </Routes>
    </Suspense>
  );
}

export default AppRoutes;
