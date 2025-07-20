import { Header, SearchForm, ProductCard } from '@components';
import styles from './MainPage.module.css';

import { useState } from 'react';
import { ProductsApi } from '@api';
import { Spinner } from '@chakra-ui/react';
import { useEffect } from 'react';

const DEFAULT_FORM = {};

export const MainPage = () => {
  const [isMounted, setIsMounted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const [form, setForm] = useState(DEFAULT_FORM);
  const [products, setProducts] = useState([]);

  const hasProducts = products.length > 0;

  const onFormChange = (form) => {
    setForm(form);
  };

  const fetchProducts = async () => {
    try {
      setIsLoading(true);
      const api = new ProductsApi();
      const products = await api.getProducts(form);
      setProducts(products);
    } catch (error) {
      /* empty */
    } finally {
      setIsLoading(false);
    }
  };

  const onFormSubmit = async () => {
    await fetchProducts();
  };

  useEffect(() => {
    if (!isMounted) {
      setIsMounted(true);
      fetchProducts(DEFAULT_FORM);
    }
  }, [isMounted, fetchProducts]);

  return (
    <div className={styles.page}>
      <Header />
      <main className={styles.main}>
        <SearchForm form={form} onChange={onFormChange} onSubmit={onFormSubmit} />
        {isLoading ? (
          <div className={styles.loader}>
            <Spinner size="xl" color="#BCCA8D" borderWidth="2px" />
          </div>
        ) : hasProducts ? (
          <ul className={styles.list}>
            {products.map((product, index) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </ul>
        ) : (
          <p className={styles.placeholder}>По вашему запросу ничего не найдено</p>
        )}
      </main>
    </div>
  );
};
