import {
  AppBar,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
  List,
  Drawer,
  Grid,
  ListItemButton,
  ListItemText,
} from "@mui/material";
import { useTranslation } from "react-i18next";
import MenuIcon from "@mui/icons-material/Menu";
import React, { useState } from "react";
import LanguageIcon from "@mui/icons-material/Language";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import { Link } from "react-router-dom";
import { TitlePortal } from "./TitlePortal";
import { Me } from "../../types/me.ts";
import {LoginButton} from "./Login.tsx";

interface HeaderProps {
  me: Me;
}
/**
 * The header component for the application that will be rendered at the top of the page.
 * @returns - The header component
 */
export function Header({ me }: HeaderProps): JSX.Element {
  const API_URL = import.meta.env.VITE_APP_API_HOST;
  const { t, i18n } = useTranslation("translation", { keyPrefix: "header" });
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

  const [open, setOpen] = useState(false);
  const [listItems, setListItems] = useState([
    { link: "/", text: t("homepage") },
  ]);

  const [anchorEl, setAnchorEl] = React.useState<null | HTMLButtonElement>(
    null,
  );

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  React.useEffect(() => {
    const baseItems = [{ link: "/", text: t("homepage") }];
    const additionalItems = [
      { link: "/projects", text: t("myProjects") },
      { link: "/courses", text: t("myCourses") },
    ];
    if (me.loggedIn) {
      setListItems([...baseItems, ...additionalItems]);
    } else {
      setListItems(baseItems);
    }
  }, [me, t]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="sticky">
        <Toolbar disableGutters>
          <IconButton
            edge="start"
            onClick={() => setOpen(!open)}
            sx={{ color: "white", marginLeft: 0 }}
          >
            <MenuIcon style={{ fontSize: "2rem" }} />
          </IconButton>
          <Link to={`/home`}
            style={{ color: 'inherit', textDecoration: 'none' }}>
            <Typography
              variant="h6"
              color="inherit"
              sx={{ marginRight: '2rem' }}>
              Peristerónas
            </Typography>
          </Link>
          <TitlePortal />
          {!me.loggedIn && (
            <LoginButton/>
          )}
          {me.loggedIn && (
            <>
              <IconButton
                edge="end"
                onClick={handleClick}
                sx={{ color: "inherit", marginRight: "0.3rem" }}
              >
                <AccountCircleIcon />
                <Typography variant="body1" sx={{ paddingLeft: "0.3rem" }}>
                  {me.display_name}
                </Typography>
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={() => setAnchorEl(null)}
              >
                <Typography sx={{ padding: "6px 16px", color: "black" }}>
                  {me.display_name}
                </Typography>
                <MenuItem>
                  <Link to={`${API_URL}/logout`} style={{ color: 'inherit', textDecoration: 'none' }}>
                    {t("logout")}</Link>
                </MenuItem>
              </Menu>
            </>
          )}
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
      <DrawerMenu
        open={open}
        onClose={() => setOpen(false)}
        listItems={listItems}
      />
    </Box>
  );
}

/**
 * Renders the drawer menu component.
 * @param open - Whether the drawer menu is open or not.
 * @param onClose - Function to handle the close event of the drawer menu.
 * @param listItems - Array of objects representing the list items in the drawer menu.
 * @returns The Side Bar
 */
function DrawerMenu({
  open,
  onClose,
  listItems,
}: {
  open: boolean;
  onClose: () => void;
  listItems: { link: string; text: string }[];
}) {
  return (
    <Drawer open={open} anchor="left" onClose={onClose}>
      <Grid
        container
        direction="column"
        sx={{
          width: 250,
          height: "100%",
          backgroundColor: "primary.main",
        }}
      >
        <Grid item container direction="row" alignItems="flex-start">
          <IconButton
            onClick={onClose}
            sx={{
              color: "white",
            }}
          >
            <MenuIcon style={{ fontSize: "2rem" }} />
          </IconButton>
        </Grid>
        <List>
          {listItems.map((listItem, index) => (
            <ListItemButton
              key={index}
              component={Link}
              to={listItem.link}
              role="listitem"
              onClick={onClose}
            >
              <ListItemText primary={listItem.text} sx={{ color: "white" }} />
            </ListItemButton>
          ))}
        </List>
      </Grid>
    </Drawer>
  );
}
