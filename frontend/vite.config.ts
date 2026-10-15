import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5175,
    proxy: {
      '/api': {
        target: 'http://localhost:8005',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8005',
        changeOrigin: true,
      }
    }
  }
})
