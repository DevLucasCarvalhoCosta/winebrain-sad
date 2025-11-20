/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
        },
        wine: {
          50: '#fdf2f7',
          100: '#fce7f1',
          200: '#fad0e5',
          300: '#f6a8cf',
          400: '#f072ad',
          500: '#e5478f',
          600: '#d1266e',
          700: '#b61955',
          800: '#961745',
          900: '#7d183c',
        }
      }
    },
  },
  plugins: [],
}
