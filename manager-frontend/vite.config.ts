import babel from "@rolldown/plugin-babel";
import react, { reactCompilerPreset } from "@vitejs/plugin-react";
import { resolve } from "path";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
	resolve: {
		alias: { "@": resolve(__dirname, "src") },
	},
	plugins: [
		react(),
		babel({
			presets: [reactCompilerPreset()],
			exclude: [/node_modules/, /src\/api/],
		}),
	],
	server: {
		watch: { usePolling: true },
		hmr: { clientPort: 3000 },
		proxy: {
			"/api/v1": "http://manager-backend:8000",
		},
	},
});
