import { Outlet } from 'react-router-dom';
import Header from '@/components/common/Header';
import Sidebar from '@/components/common/Sidebar';
import Footer from '@/components/common/Footer';

/**
 * Main layout that wraps all protected pages.
 * Uses a responsive two‑column layout with a collapsible sidebar.
 */
function MainLayout() {
  return (
    <div className="flex min-h-screen bg-surface-900 text-surface-50">
      {/* Sidebar */}
      <Sidebar />
      {/* Main content area */}
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header />
        <main className="flex-1 p-6 overflow-auto">
          {/* Render the matched route component */}
          <Outlet />
        </main>
        <Footer />
      </div>
    </div>
  );
}

export default MainLayout;
