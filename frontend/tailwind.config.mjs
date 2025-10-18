/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // usa nomes compatíveis com Tailwind padrão
        primary: {
          DEFAULT: "#003366",
          dark: "#002244",
          light: "#0066cc",
        },
        neutral: {
          DEFAULT: "#6b7280",
          light: "#f3f4f6",
          dark: "#374151",
        },
      },
    },
  },
  plugins: [],
};
