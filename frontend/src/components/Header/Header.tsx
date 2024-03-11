import {
  AppBar,
  Box,
  Button,
  Toolbar,
  Typography
} from "@mui/material";
import Navbar from "./Navbar";
import { useTranslation } from 'react-i18next';
/**
 * The header component for the application that will be rendered at the top of the page.
 * @returns - The header component
 */
export function Header(): JSX.Element {
  const { t } = useTranslation();

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="sticky">
        <Toolbar>
          <Box sx={{ flexGrow: 1 }}>
            <Navbar />
          </Box>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {t('home')}
          </Typography>
          <Button color="inherit">{t('login')}</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}