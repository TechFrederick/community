/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    // There are some Tailwind classes embedded in the frontend Python module.
    "./community/frontend.py",
  ],
  theme: {
    extend: {
      colors: {
        tfdarkblue: '#143962',
        tflightblue: '#1f92c9',
        tfgreen: '#a0cf60',
      },
    },
  },
  plugins: [],
}

