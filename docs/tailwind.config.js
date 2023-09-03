/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./theme.config.jsx"
  ],
  darkMode: 'class',
  theme: {
    extend: {},
    fontFamily: {
      mono: [
        "'Ubuntu Mono'",
        "monospace"
      ]
    }
  },
  plugins: [],
}
