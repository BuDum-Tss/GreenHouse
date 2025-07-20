import { Button, Dialog, Portal } from '@chakra-ui/react';
import { ProductList } from '../ProductList';
import { useCart } from '../../context';

export const CartModal = ({ trigger, isOpen, onOpen }) => {
  const { cartItems, addToCart, removeFromCart } = useCart();

  const onAddToCart = (product) => {
    addToCart(product);
  };

  const onRemoveFromCart = (id) => {
    removeFromCart(id);
  };

  const onModalOpen = (event) => {
    onOpen(event.open);
  };

  return (
    <Dialog.Root lazyMount size="cover" open={isOpen} onOpenChange={onModalOpen}>
      <Dialog.Trigger asChild>{trigger}</Dialog.Trigger>
      <Portal>
        <Dialog.Backdrop />
        <Dialog.Positioner padding="16px">
          <Dialog.Content>
            <Dialog.Header>
              <Dialog.Title fontWeight={400} fontSize="20px">
                Оформление заказа
              </Dialog.Title>
            </Dialog.Header>
            <Dialog.Body>
              <ProductList products={cartItems} onIncrease={onAddToCart} onDecrease={onRemoveFromCart} />
            </Dialog.Body>
            <Dialog.Footer>
              <Dialog.ActionTrigger asChild>
                <Button backgroundColor="white" borderColor="#9E9E9E" color="#9E9E9E">
                  Закрыть
                </Button>
              </Dialog.ActionTrigger>
              <Button backgroundColor="#BCCA8D" color="white">
                Оформить
              </Button>
            </Dialog.Footer>
          </Dialog.Content>
        </Dialog.Positioner>
      </Portal>
    </Dialog.Root>
  );
};
