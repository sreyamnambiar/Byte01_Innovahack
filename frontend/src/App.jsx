/**
 * DarkTrust – Root Application Component
 *
 * Wraps the application with:
 * - BrowserRouter for client-side routing
 * - Global context providers (added as modules are developed)
 * - Route definitions from the centralized routes module
 */

import { BrowserRouter } from 'react-router-dom';
import AppRoutes from '@/routes';

/**
 * App component.
 *
 * This is the top-level component mounted by main.jsx.
 * Add global context providers here as the platform grows:
 *
 *   <AuthProvider>
 *     <ThemeProvider>
 *       <NotificationProvider>
 *         <BrowserRouter>
 *           <AppRoutes />
 *         </BrowserRouter>
 *       </NotificationProvider>
 *     </ThemeProvider>
 *   </AuthProvider>
 */
function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}

export default App;
