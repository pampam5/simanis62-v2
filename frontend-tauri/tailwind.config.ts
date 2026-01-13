import type { Config } from 'tailwindcss';

export default {
    // Force dark mode to only activate with the "dark" class
    // This prevents system preference from taking over
    darkMode: 'class',
    content: [
        './index.html',
        './src/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
} satisfies Config;
