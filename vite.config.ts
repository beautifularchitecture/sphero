import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite build for the u3-stats-ui SPA. Sources live under frontend/; the built
// static bundle is emitted to dist/ at the workspace root so U1's FastAPI backend
// can serve it as static files.
export default defineConfig({
  root: 'frontend',
  plugins: [react()],
  build: {
    outDir: '../dist',
    emptyOutDir: true,
  },
});
