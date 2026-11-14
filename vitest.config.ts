import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

// vitest.config.ts lives at the workspace root per the u3-stats-ui testing contract.
// Tests are co-located under frontend/src and matched by the unit filter below,
// so `vitest run` from the workspace root executes u3-stats-ui tests only — never
// a bare project-wide command.
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    include: ['frontend/src/**/*.test.{ts,tsx}'],
    // Register jest-dom matchers (toBeInTheDocument, toBeDisabled, ...) used by
    // the u3-stats-ui BDD scenarios. @testing-library/jest-dom is a declared
    // devDependency; this setup file extends vitest's expect for every test.
    setupFiles: ['./frontend/src/test-setup.ts'],
  },
});
