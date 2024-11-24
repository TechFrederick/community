/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/**/*.html",
    // There are some Tailwind classes embedded in the frontend Python module.
    "../techcity/core/frontend.py",
  ],
  theme: {
    extend: {
      colors: {
        tcdarkblue: '#143962',
        tclightblue: '#1f92c9',
        tcgreen: '#a0cf60',
      },
    },
  },
  plugins: [],
}
