/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/home.html"],
  theme: {
    extend: {
      fontFamily: {
        yellowtail: ["YELLOWTAIL", "cursive"],
        gothic: ["LEAGUEGOTHIC", "sans-serif"],
      },
    },
  },
  plugins: [],
}
