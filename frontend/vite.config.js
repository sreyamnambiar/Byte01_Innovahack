import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath, URL } from 'node:url';

/**
 * DarkTrust – Vite Configuration
 *
 * @see https://vitejs.dev/config/
 */

/** Helper: resolve paths relative to this config file using ESM-safe URL API */
const r = (/** @type {string} */ p) => fileURLToPath(new URL(p, import.meta.url));

export default defineConfig({
  plugins: [
    react(),
  ],

  // ── Path Aliases ──────────────────────────────────────────────────────
  // Enables clean imports like `import Button from '@/components/Button'`
  // instead of `../../components/Button`.
  resolve: {
    alias: {
      '@':           r('./src'),
      '@components': r('./src/components'),
      '@pages':      r('./src/pages'),
      '@layouts':    r('./src/layouts'),
      '@hooks':      r('./src/hooks'),
      '@context':    r('./src/context'),
      '@services':   r('./src/services'),
      '@utils':      r('./src/utils'),
      '@assets':     r('./src/assets'),
      '@routes':     r('./src/routes'),
    },
  },

  // ── Development Server ────────────────────────────────────────────────
  server: {
    port: 5173,
    strictPort: false,
    open: false,

    // Proxy API requests to the FastAPI backend during development.
    // This avoids CORS issues in development.
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },

  // ── Build Configuration ────────────────────────────────────────────────
  build: {
    outDir: 'dist',
    sourcemap: true,
    // Raise the chunk size warning threshold slightly for enterprise apps
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        // Split vendor code into separate chunks for better caching.
        // Vite 8 / rolldown requires manualChunks as a function.
        manualChunks(id) {
          if (id.includes('node_modules/react') || id.includes('node_modules/react-dom')) {
            return 'vendor';
          }
          if (id.includes('node_modules/react-router')) {
            return 'router';
          }
          if (id.includes('node_modules/axios')) {
            return 'http';
          }
        },
      },
    },
  },

  // ── CSS ───────────────────────────────────────────────────────────────
  css: {
    devSourcemap: true,
  },
});
