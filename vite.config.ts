import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite build for the u3-stats-ui SPA. Sources live under frontend/; the built
// static bundle is emitted to dist/ at the workspace root so U1's FastAPI backend
// can serve it as static files.
export default defineConfig({
  root: 'frontend',
  plugins: [react()],
  // Dev-only: the SPA derives both WebSocket URLs from its own origin, so
  // forward them to the two backend processes started by backend.sh.
  server: {
    proxy: {
      '/ws/chat': { target: 'ws://127.0.0.1:8000', ws: true },
      '/ws/robot-state': { target: 'ws://127.0.0.1:8001', ws: true },
    },
  },
  build: {
    outDir: '../dist',
    emptyOutDir: true,
  },
});
