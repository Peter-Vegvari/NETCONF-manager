import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] })
  ],
  server: {
    watch: { usePolling: true },
    hmr: { clientPort: 3000 },
    proxy: {
      '/connect': 'http://manager-backend:8000',
      '/modules': 'http://manager-backend:8000',
    },
  },
})
