import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';

const root = document.getElementById('root');
if (!root) {
  throw new Error('StatsPanel mount point #root not found');
}

createRoot(root).render(
  <App />
);
