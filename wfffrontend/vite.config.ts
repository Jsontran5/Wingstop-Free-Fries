import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";


// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  server: {
    host: "::",
    port: 8080,
    proxy: {
      // React Router routes - bypass to serve index.html for SPA
      '/restaurant': {
        bypass: () => '/index.html'
      },
      '/result': {
        bypass: () => '/index.html'  
      },
      '/stats': {
        bypass: () => '/index.html'
      },
      '/error': {
        bypass: () => '/index.html'
      },
      
      // API endpoints
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
      // Flask admin/utility routes
      '/updatecoupondatabase': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/deleteexpiredcoupons': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/fetchcoupons': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/sendfeedback': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/statistics': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/pandaemail': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/wingstopemail': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/blazeemail': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/bruincardnfcpandalightningsubmit': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/bruincardnfcwingstoplightningsubmit': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/aprilfools': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/afannouncement': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      // Legacy HTML routes
      '/wingstop': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/rubios': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/r': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/pandaexpress': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/panda': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/pe': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/blazepizza': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/bp': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/dunkin': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/donuts': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/dd': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      // Lightning routes
      '/pandalightning': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/wingstoplightning': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/pandalightningsubmit': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/wingstoplightningsubmit': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/pandalightningresult': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/wingstoplightningresult': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      // Utility routes
      '/submit': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/robots.txt': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    }
  },
  plugins: [
    react(),
    
  ].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
