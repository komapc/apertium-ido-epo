import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Use the Firebase project ID from env or fallback to .firebaserc default
const FIREBASE_PROJECT_ID = process.env.FIREBASE_PROJECT_ID || 'ido-epo-translator'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        // Route Vite dev requests to the local Functions emulator path
        rewrite: (path) => `/${FIREBASE_PROJECT_ID}/us-central1${path}`
      }
    }
  }
})

