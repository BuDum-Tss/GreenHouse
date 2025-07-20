import styles from './CartLayout.module.css';
import { IconButton } from '@chakra-ui/react';
import { ShoppingBagIcon } from '@phosphor-icons/react';
import { useCart } from '@context';
import { CartModal } from '../CartModal';
import { useState } from 'react';

export const CartLayout = ({ children }) => {
  const { totalItems } = useCart();

  const [isOpen, setIsOpen] = useState(false);

  const hasCartButton = totalItems > 0;

  const onModalToggle = (isOpen) => {
    setIsOpen(isOpen);
  };

  return (
    <div className={styles.layout}>
      {children}
      {hasCartButton && (
        <CartModal
          isOpen={isOpen}
          onOpen={onModalToggle}
          trigger={
            <IconButton
              rounded={50}
              backgroundColor="white"
              border="1px solid #9E9E9E"
              size="xl"
              position="absolute"
              bottom="8px"
              right="8px"
            >
              <ShoppingBagIcon color="#9E9E9E" size={32} />
              <div className={styles.counter}>{totalItems}</div>
            </IconButton>
          }
        />
      )}
    </div>
  );
};
