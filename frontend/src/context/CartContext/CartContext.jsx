import { createContext, useState } from 'react';

// Создаем контекст
export const CartContext = createContext();

// Провайдер корзины
export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);

  // Добавление товара в корзину
  const addToCart = (product) => {
    setCartItems((prevItems) => {
      // Проверяем, есть ли товар уже в корзине
      const existingItem = prevItems.find((item) => item.id === product.id);

      if (existingItem) {
        // Если есть, увеличиваем количество
        return prevItems.map((item) => (item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item));
      } else {
        // Если нет, добавляем новый товар
        return [...prevItems, { ...product, quantity: 1 }];
      }
    });
  };

  // Удаление товара из корзины
  const removeFromCart = (productId) => {
    setCartItems((prevItems) => {
      // Находим товар
      const existingItem = prevItems.find((item) => item.id === productId);

      if (existingItem.quantity === 1) {
        // Если количество 1, удаляем товар полностью
        return prevItems.filter((item) => item.id !== productId);
      } else {
        // Иначе уменьшаем количество
        return prevItems.map((item) => (item.id === productId ? { ...item, quantity: item.quantity - 1 } : item));
      }
    });
  };

  // Полное удаление товара (независимо от количества)
  const deleteFromCart = (productId) => {
    setCartItems((prevItems) => prevItems.filter((item) => item.id !== productId));
  };

  // Очистка корзины
  const clearCart = () => {
    setCartItems([]);
  };

  // Общее количество товаров в корзине
  const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  // Общая стоимость товаров в корзине
  const totalPrice = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        cartItems,
        addToCart,
        removeFromCart,
        deleteFromCart,
        clearCart,
        totalItems,
        totalPrice,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};
