import { MinusIcon, PlusIcon } from '@phosphor-icons/react';
import styles from './ProductItem.module.css';
import { IconButton } from '@chakra-ui/react';

export const ProductItem = ({ product, onIncrease, onDecrease }) => {
  const totalPrice = product.quantity * product.price;

  console.log(onIncrease);

  return (
    <li className={styles.item}>
      <span className={styles.name}>{product.name}</span>
      <div className={styles.group}>
        <div className={styles.quantityControls}>
          <div>
            <IconButton rounded={50} backgroundColor="#bcca8d" size="xs" onClick={() => onDecrease(product.id)}>
              <MinusIcon color="white" size={16} />
            </IconButton>
            <span className={styles.quantity}>{product.quantity}</span>
            <IconButton rounded={50} backgroundColor="#bcca8d" size="xs" onClick={() => onIncrease(product)}>
              <PlusIcon color="white" size={16} />
            </IconButton>
          </div>

          <span className={styles.price}>{totalPrice} р.</span>
        </div>
      </div>
    </li>
  );
};
