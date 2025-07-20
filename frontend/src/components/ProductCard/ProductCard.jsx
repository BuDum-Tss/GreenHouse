import { Button } from '@chakra-ui/react';
import styles from './ProductCard.module.css';
import Boul from '@assets/Boul.jpg';
import { useCart } from '@context';

export const ProductCard = ({ product }) => {
  const { addToCart } = useCart();

  const onAddToCart = () => {
    addToCart(product);
  };

  return (
    <li className={styles.card}>
      <figure className={styles.figure}>
        <a className="movies-card__link" target="_blank" rel="noreferrer">
          <img className={styles.image} src={Boul} />
        </a>
        <figcaption className={styles.figcaption}>
          <div className={styles.text}>
            <div className={styles.row}>
              <h2 className={styles.name}>{product.name}</h2>
            </div>
            <p className={styles.description}>{product.description}</p>
          </div>
          <div className={styles.row}>
            <p className={styles.price}>{product.price} р.</p>
            <Button rounded={8} flex={1} backgroundColor="#BCCA8D" alignSelf="flex-end" onClick={onAddToCart}>
              Добавить в корзину
            </Button>
          </div>
        </figcaption>
      </figure>
    </li>
  );
};
