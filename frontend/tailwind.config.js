/** @type {import('tailwindcss').Config} */

/**
 * DarkTrust – Tailwind CSS Configuration
 *
 * Defines the DarkTrust design system:
 * - Dark cyber-security color palette
 * - Custom typography scale
 * - Animation utilities
 * - Extended spacing and border radius
 */
export default {
  // Scan all JSX/JS files for class names
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],

  // Dark mode via class strategy (.dark on <html>)
  darkMode: 'class',

  theme: {
    extend: {

      // ── DarkTrust Color Palette ───────────────────────────────────────
      colors: {
        // Primary brand – electric cyan/teal
        primary: {
          50:  '#e0fffe',
          100: '#b3fffe',
          200: '#80fffc',
          300: '#4dfff9',
          400: '#26fff7',
          500: '#00f5f0',   // Core brand color
          600: '#00c4be',
          700: '#00928d',
          800: '#00615d',
          900: '#002f2d',
          950: '#001514',
        },

        // Accent – electric violet
        accent: {
          50:  '#f0e6ff',
          100: '#d4b3ff',
          200: '#b980ff',
          300: '#9d4dff',
          400: '#8226ff',
          500: '#6600ff',   // Core accent
          600: '#5200cc',
          700: '#3d0099',
          800: '#290066',
          900: '#140033',
          950: '#0a001a',
        },

        // Surface / Background layers (dark UI)
        surface: {
          50:  '#e8eaf0',
          100: '#c5c9d8',
          200: '#9fa6bc',
          300: '#7883a0',
          400: '#5a6589',
          500: '#3d4872',
          600: '#2e3560',
          700: '#1e2347',  // Card backgrounds
          800: '#141830',  // Elevated surfaces
          900: '#0c0f1e',  // Page background
          950: '#060810',  // Deepest background
        },

        // Status colors
        success: {
          400: '#34d399',
          500: '#10b981',
          600: '#059669',
        },
        warning: {
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
        },
        danger: {
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
        },
        info: {
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
        },

        // Trust score colors (Zero Trust specific)
        trust: {
          critical: '#ef4444',  // 0–20  – deny
          low:      '#f97316',  // 21–40 – high risk
          medium:   '#eab308',  // 41–60 – elevated
          high:     '#22c55e',  // 61–80 – trusted
          verified: '#00f5f0',  // 81–100 – verified
        },
      },

      // ── Typography ────────────────────────────────────────────────────
      fontFamily: {
        sans:  ['Inter', 'system-ui', 'sans-serif'],
        mono:  ['JetBrains Mono', 'Fira Code', 'monospace'],
        display: ['Outfit', 'Inter', 'sans-serif'],
      },

      // ── Box Shadows (glassmorphism + glow effects) ────────────────────
      boxShadow: {
        'glow-primary': '0 0 20px rgba(0, 245, 240, 0.3)',
        'glow-accent':  '0 0 20px rgba(102, 0, 255, 0.3)',
        'glow-danger':  '0 0 20px rgba(239, 68, 68, 0.3)',
        'glow-success': '0 0 20px rgba(16, 185, 129, 0.3)',
        'glass':        '0 8px 32px rgba(0, 0, 0, 0.4)',
        'card':         '0 4px 24px rgba(0, 0, 0, 0.3)',
        'inner-glow':   'inset 0 1px 0 rgba(255, 255, 255, 0.1)',
      },

      // ── Background (glassmorphism) ────────────────────────────────────
      backdropBlur: {
        xs: '2px',
      },

      // ── Animations ────────────────────────────────────────────────────
      animation: {
        'fade-in':       'fadeIn 0.3s ease-in-out',
        'fade-in-up':    'fadeInUp 0.4s ease-out',
        'fade-in-down':  'fadeInDown 0.4s ease-out',
        'slide-in-left': 'slideInLeft 0.3s ease-out',
        'pulse-slow':    'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-pulse':    'glowPulse 2s ease-in-out infinite',
        'spin-slow':     'spin 3s linear infinite',
        'scan-line':     'scanLine 2s linear infinite',
        'float':         'float 3s ease-in-out infinite',
      },

      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%':   { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInDown: {
          '0%':   { opacity: '0', transform: 'translateY(-16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          '0%':   { opacity: '0', transform: 'translateX(-16px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 10px rgba(0, 245, 240, 0.3)' },
          '50%':      { boxShadow: '0 0 30px rgba(0, 245, 240, 0.7)' },
        },
        scanLine: {
          '0%':   { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%':      { transform: 'translateY(-8px)' },
        },
      },

      // ── Border Radius ─────────────────────────────────────────────────
      borderRadius: {
        'xl2': '1.25rem',
        'xl3': '1.5rem',
      },

      // ── Z-index ───────────────────────────────────────────────────────
      zIndex: {
        '60':  '60',
        '70':  '70',
        '80':  '80',
        '90':  '90',
        '100': '100',
      },
    },
  },

  plugins: [],
};
