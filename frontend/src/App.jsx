import { ChakraProvider, createSystem, defaultConfig } from '@chakra-ui/react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import { MainPage } from './pages';
import { CartLayout } from './components';
import { CartProvider } from './context';
import '@fontsource-variable/montserrat/index.css';

function App() {
  const system = createSystem(defaultConfig, {
    theme: {
      tokens: {
        fonts: {
          heading: { value: 'Montserrat Variable' },
          body: { value: 'Montserrat Variable' },
        },
      },
    },
  });

  return (
    <CartProvider>
      <ChakraProvider value={system}>
        <BrowserRouter>
          <CartLayout>
            <Routes>
              <Route path="/" element={<MainPage />} />
            </Routes>
          </CartLayout>
        </BrowserRouter>
      </ChakraProvider>
    </CartProvider>
  );
}

export default App;
