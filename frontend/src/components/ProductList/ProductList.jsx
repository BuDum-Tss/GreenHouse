import { ProductItem } from '../ProductItem';
import styles from './ProductList.module.css';

export const ProductList = ({ products, onIncrease, onDecrease }) => {
  return (
    <ul className={styles.list}>
      {products.map((product) => (
        <ProductItem key={product.id} product={product} onIncrease={onIncrease} onDecrease={onDecrease} />
      ))}
    </ul>
  );
};
