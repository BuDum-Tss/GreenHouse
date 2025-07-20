import { IconButton } from '@chakra-ui/react';
import { MagnifyingGlassIcon } from '@phosphor-icons/react';
import styles from './SearchForm.module.css';

export const SearchForm = ({ form, onChange, onSubmit }) => {
  const { prompt = '' } = form;

  const onInputChange = (event) => {
    onChange({ ...form, prompt: event.target.value });
  };

  const onFormSubmit = (event) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <form className={styles.searchForm} onSubmit={onFormSubmit}>
      <div className={styles.inputWrapper}>
        <input className={styles.input} placeholder="Введите ваш запрос" value={prompt} onChange={onInputChange} />
        <IconButton
          type="submit"
          position="absolute"
          top="8px"
          right="8px"
          rounded={50}
          backgroundColor="#bcca8d"
          size="xs"
        >
          <MagnifyingGlassIcon color="white" size={16} />
        </IconButton>
      </div>
    </form>
  );
};
