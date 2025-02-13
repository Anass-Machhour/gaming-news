import type { Config } from "tailwindcss";

export default {
	content: [
		"./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
		"./src/components/**/*.{js,ts,jsx,tsx,mdx}",
		"./src/app/**/*.{js,ts,jsx,tsx,mdx}",
	],
	theme: {
		extend: {
			colors: {
				background: "var(--background)",
				foreground: "var(--foreground)",
			},
			gridTemplateColumns: {
				// Simple 16 column grid
				"resp-grid": "repeat(auto-fit, minmax(min(200px, 100%), 1fr))",
			},
			backgroundImage: {
				"custom-img": "url('../../public/images/Neon_Gaming.png')",
			},
		},
	},
	plugins: [],
} satisfies Config;
