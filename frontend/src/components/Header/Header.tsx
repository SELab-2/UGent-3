import {
  AppBar,
  Box,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import LanguageIcon from '@mui/icons-material/Language';

/**
 * The header component for the application that will be rendered at the top of the page.
 * @returns - The header component
 */
export function Header(): JSX.Element {
  const { t, i18n } = useTranslation();
  const [languageMenuAnchor, setLanguageMenuAnchor] =
    useState<null | HTMLElement>(null);

  const handleLanguageMenu = (event: React.MouseEvent<HTMLElement>) => {
    setLanguageMenuAnchor(event.currentTarget);
  };

  const handleChangeLanguage = (language: string) => {
    i18n.changeLanguage(language);
    setLanguageMenuAnchor(null);
  }

  const handleCloseLanguageMenu = () => {
    setLanguageMenuAnchor(null);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="sticky">
        <Toolbar>
          <IconButton size="large" color="inherit">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {t("home")}
          </Typography>
          <Button color="inherit">{t("login")}</Button>
          <div>
            <IconButton onClick={handleLanguageMenu} color="inherit">
              <LanguageIcon />
              <Typography style={{marginLeft: "0.3rem"}}>{t("tag")}</Typography>
            </IconButton>
            <Menu
                anchorEl={languageMenuAnchor}
                open={Boolean(languageMenuAnchor)}
                onClose={handleCloseLanguageMenu}
              >
                <MenuItem onClick={() => handleChangeLanguage("en")}>English</MenuItem>
                <MenuItem onClick={() => handleChangeLanguage("nl")}>Nederlands</MenuItem>
              </Menu>
          </div>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
