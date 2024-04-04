import {
  AppBar,
  Box,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
  List,
  Drawer,
  Grid,
  ListItemButton,
  ListItemText
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { useTranslation } from 'react-i18next';
import { useEffect, useState } from "react";
import LanguageIcon from "@mui/icons-material/Language";
import { Link, useLocation } from "react-router-dom";

/**
 * The header component for the application that will be rendered at the top of the page.
 * @returns - The header component
 */
export function Header(): JSX.Element {
  const { t, i18n } = useTranslation('translation', { keyPrefix: 'header' });
  const [languageMenuAnchor, setLanguageMenuAnchor] =
    useState<null | HTMLElement>(null);

  const handleLanguageMenu = (event: React.MouseEvent<HTMLElement>) => {
    setLanguageMenuAnchor(event.currentTarget);
  };

  const handleChangeLanguage = (language: string) => {
    i18n.changeLanguage(language);
    setLanguageMenuAnchor(null);
  };

  const handleCloseLanguageMenu = () => {
    setLanguageMenuAnchor(null);
  };

  const location = useLocation();
  const [open, setOpen] = useState(false);
  const [listItems, setListItems] = useState([
    { link: "/", text: t("homepage") }
  ]);

  useEffect(() => {
    const baseItems = [{ link: "/", text: t("homepage") }];
    const additionalItems = [
      { link: "/projects", text: t("myProjects") },
      { link: "/courses", text: t("myCourses") }
    ];
    if (isLoggedIn()) {
      setListItems([...baseItems, ...additionalItems]);
    }
    else {
      setListItems(baseItems);
    }
  }, [t]);

  const title = getTitle(location.pathname, t);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="sticky">
        <Toolbar disableGutters>
          <IconButton edge="start" onClick={() => setOpen(!open)} sx={{ color: "white", marginLeft: 0 }}>
            <MenuIcon style={{fontSize:"2rem"}} />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {title}
          </Typography>
          <Button color="inherit">{t("login")}</Button>
          <div>
            <IconButton onClick={handleLanguageMenu} color="inherit">
              <LanguageIcon />
              <Typography style={{ marginLeft: "0.3rem" }}>
                {t("tag")}
              </Typography>
            </IconButton>
            <Menu
              anchorEl={languageMenuAnchor}
              open={Boolean(languageMenuAnchor)}
              onClose={handleCloseLanguageMenu}
            >
              <MenuItem onClick={() => handleChangeLanguage("en")}>
                English
              </MenuItem>
              <MenuItem onClick={() => handleChangeLanguage("nl")}>
                Nederlands
              </MenuItem>
            </Menu>
          </div>
        </Toolbar>
      </AppBar>
      <DrawerMenu open={open} onClose={() => setOpen(false)} listItems={listItems}/>
    </Box>
  );
}
/**
 * @returns Whether a user is logged in or not.
 */
function isLoggedIn() {
  return true;
}

/**
 * Get the title based on the given pathname.
 * @param pathname - The current pathname.
 * @param t - The translation function.
 * @returns The title.
 */
function getTitle(pathname: string, t: (key: string) => string): string {
  switch(pathname) {
  case '/': return t('home');
  case '/login': return t('login');
  case '/courses': return t('myCourses');
  case '/projects': return t('myProjects');
  case '/dummy-create-project': return t('projectUploadForm')
  default: return t('home');
  }
}

/**
 * Renders the drawer menu component.
 * @param open - Whether the drawer menu is open or not.
 * @param onClose - Function to handle the close event of the drawer menu.
 * @param listItems - Array of objects representing the list items in the drawer menu.
 * @returns The Side Bar
 */
function DrawerMenu({ open, onClose, listItems }: { open: boolean, onClose: () => void, listItems: { link: string, text: string }[] }) {

  return (
    <Drawer open={open} anchor="left" onClose={onClose}>
      <Grid container direction="column" sx={{
        width: 250,
        height: "100%",
        backgroundColor: "primary.main"
      }}>
        <Grid item container direction="row" alignItems="flex-start">
          <IconButton onClick={onClose} sx={{
            color: "white"
          }}>
            <MenuIcon style={{fontSize:"2rem"}} />
          </IconButton>
        </Grid>
        <List>
          {listItems.map((listItem, index) => (
            <ListItemButton key={index} component={Link} to={listItem.link} role="listitem" onClick={onClose}>
              <ListItemText primary={listItem.text} sx={{color:"white"}} />
            </ListItemButton>
          ))}
        </List>
      </Grid>
    </Drawer>
  );
}
