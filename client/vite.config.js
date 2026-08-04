import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/generate': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
