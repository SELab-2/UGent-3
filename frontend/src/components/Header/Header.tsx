import { AppBar, Box, Button, Drawer, Grid, IconButton, List, ListItemButton, ListItemText, Toolbar, Typography } from "@mui/material";
import { Menu } from "@mui/icons-material";
import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';
import { useState } from "react";

/**
 * Renders the header component.
 * @returns JSX.Element representing the header.
 */
export function Header(): JSX.Element {
  const { t } = useTranslation();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  const listItems = [
    {link: "/", text: t("homepage")},
    {link: "/projects", text: t("myProjects")},
    {link: "/courses", text: t("myCourses")}
  ]

  const title = getTitle(location.pathname, t);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="sticky">
        <Toolbar disableGutters>
          <IconButton edge="start" onClick={() => setOpen(!open)} sx={{ color: "white", marginLeft: 0 }}>
            <Menu style={{fontSize:"2rem"}} />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 0 }}>
            {title}
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Button color="inherit">{t('login')}</Button>
        </Toolbar>
      </AppBar>
      <DrawerMenu open={open} onClose={() => setOpen(false)} listItems={listItems} />
    </Box>
  );
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
            <Menu style={{fontSize:"2rem"}} />
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
