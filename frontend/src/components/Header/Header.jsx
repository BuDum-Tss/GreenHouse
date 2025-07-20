import { Button, IconButton } from '@chakra-ui/react';
import styles from './Header.module.css';
import { BellIcon, UserIcon } from '@phosphor-icons/react';

export const Header = () => {
  return (
    <header className={styles.header}>
      <Button variant="plain" color="#BCCA8D" fontSize="24px" padding={0} height="fit-content">
        Теплица
      </Button>
      <div className={styles.actions}>
        <IconButton rounded={50} backgroundColor="#bcca8d" size="xs">
          <BellIcon color="white" size={16} />
        </IconButton>
        <IconButton rounded={50} backgroundColor="#bcca8d" size="xs">
          <UserIcon color="white" size={16} />
        </IconButton>
      </div>
    </header>
  );
};
