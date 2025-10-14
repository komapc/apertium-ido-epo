import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // No special proxy needed for production (Cloudflare Pages serves /api via Functions).
  // For local dev against local APy directly, you can uncomment below:
  // server: {
  //   proxy: {
  //     '/api': {
  //       target: 'http://localhost:2737',
  //       changeOrigin: true,
  //       rewrite: (path) => path
  //     }
  //   }
  // }
})

