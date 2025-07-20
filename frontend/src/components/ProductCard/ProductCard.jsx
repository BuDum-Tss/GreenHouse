import { Button } from '@chakra-ui/react';

import { useCart } from '@context';
import BoulImage from '@assets/BoulImage.jpg';

import styles from './ProductCard.module.css';
import { images } from './constants';

export const ProductCard = ({ product }) => {
  const { addToCart } = useCart();

  const image = images[product.id] ?? BoulImage;

  const onAddToCart = () => {
    addToCart(product);
  };

  return (
    <li className={styles.card}>
      <figure className={styles.figure}>
        <a className="movies-card__link" target="_blank" rel="noreferrer">
          <img className={styles.image} src={image} />
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
