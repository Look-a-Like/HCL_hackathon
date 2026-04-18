import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg:         { DEFAULT: "#F5F3FF", alt: "#EDE9FE" },
        surface:    { DEFAULT: "#FFFFFF", 2: "#F9F8FF" },
        primary: {
          DEFAULT: "#7C3AED",
          hover:   "#6D28D9",
          light:   "#8B5CF6",
          50:      "#F5F3FF",
          100:     "#EDE9FE",
          200:     "#DDD6FE",
          300:     "#C4B5FD",
        },
        ink:       { DEFAULT: "#1E1B4B", 2: "#312E81" },
        secondary: "#6B7280",
        muted:     "#9CA3AF",
        border:    "#E5E7EB",
      },
      fontFamily: {
        sans: ["'Plus Jakarta Sans'", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
