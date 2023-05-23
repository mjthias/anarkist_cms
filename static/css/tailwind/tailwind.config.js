/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: ["../../../views/*.html", "../../../views/*/*.html"],
  theme: {
    colors: {
      'danger': "rgba(220,38,37,100)",
      'success': 'rgba(23,163,74,100)',
      'background': 'rgba(14, 14,14,100)',
      'outline': 'rgba(82,82,82,100)',
      'outline-focus': 'rgba(138,138,138,100)', 
      'line': 'rgba(71,71,71,100)',
      'input-bg': 'rgba(45,45,45,100)',
      'highlight-bg': 'rgba(45,45,45,100)',
      'primary': 'rgba(255,255,255,100)',
      'secondary': 'rgba(156,156,156,100)',
      'btn': {
        'light': 'rgba(80,170,100,100)',
        'dark': 'rgba(67,146,85,100)',
        'invalid': 'rgba()'
      }
    },
    fontFamily: {
      sans: ['Barlow Semi Condensed', 'sans-serif']
    },
    extend: {},
  },
  plugins: [],
}

