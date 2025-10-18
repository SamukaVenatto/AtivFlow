/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta SENAC
        'senac-blue': {
          DEFAULT: '#003366',
          dark: '#002244',
          light: '#0066cc'
        },
        'senac-gray': {
          DEFAULT: '#6b7280',
          light: '#f3f4f6',
          dark: '#374151'
        }
      }
    },
  },
  plugins: [],
}

