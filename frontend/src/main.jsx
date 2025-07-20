import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { init, miniApp } from '@telegram-apps/sdk';
import App from './App.jsx';

import './index.css';

const initializeTelegramSDK = async () => {
  try {
    await init();

    if (miniApp.ready.isAvailable()) {
      await miniApp.ready();
      console.log('Mini App готово');
    }
  } catch (error) {
    console.error('Ошибка инициализации:', error);
  }
};

initializeTelegramSDK();

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
