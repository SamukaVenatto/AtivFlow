import { createThemes } from 'tw-colors';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'senac-blue': '#003366',
        'senac-blue-dark': '#002244',
        'senac-blue-light': '#0066cc',
        'senac-gray': '#6b7280',
        'senac-gray-light': '#f3f4f6',
        'senac-gray-dark': '#374151',
      },
    },
  },
  plugins: [],
};
