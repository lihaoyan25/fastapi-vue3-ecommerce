/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ===== 主按钮颜色=====
        primary: '#EAB308',          // 金色（相当于 tailwind 的 yellow-500）
        'primary-hover': '#D97706',  // 悬浮加深（amber-600）
        // ===== 以下保持不变 =====
        'gray-bg': '#F5F5F7',
        'text-primary': '#1D1D1F',
        'text-secondary': '#86868B',
        'text-tertiary': '#6E6E73',
        'border-light': '#D2D2D7',
        danger: '#FF3B30'
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '18px'
      },
      boxShadow: {
        'card': '0 4px 20px rgba(0, 0, 0, 0.04)',
        'card-hover': '0 8px 30px rgba(0, 0, 0, 0.08)'
      },
      transitionTimingFunction: {
        'apple': 'cubic-bezier(0.25, 0.1, 0.25, 1)'
      }
    },
  },
  plugins: [],
}
