import { useState } from "react";
import {
  IconButton,
  List,
  ListItemText,
  makeStyles,
  CssBaseline,
  Drawer,
  Grid
} from "@material-ui/core";
import { ListItemButton } from '@mui/material';
import {
  Menu
} from "@material-ui/icons";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

const useStyles = makeStyles((theme) => ({
  menuSliderContainer: {
    width: 250,
    background: "#373b42",
    height: "100%"
  },
  avatar: {
    margin: "0.5rem auto",
    padding: "1rem",
    width: theme.spacing(13),
    height: theme.spacing(13)
  },
  listItem: {
    color: "white"
  },
  iconButton: {
    color: "blue"
  }
}));

/**
 * Renders the navbar.
 * @returns - A Drawer with a list of navigation items.
 */
export default function Navbar() {
  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const toggleSlider = (openState: boolean) => () => {
    setOpen(openState);
  };
  const { t } = useTranslation();
  const listItems = [
    {link: "/", text: t("Homepage")},
    {link: "/projects", text: t("Mijn projecten")},
    {link: "/courses", text: t("Mijn vakken")}
  ]

  const SideList = () => (
    <Grid container direction="column" className={classes.menuSliderContainer}>
      <Grid item container direction="row" alignItems="flex-start">
        <IconButton onClick={toggleSlider(!open)} className={classes.iconButton}>
          <Menu style={{fontSize:"3rem"}} />
        </IconButton>
      </Grid>
      <Grid item>
      </Grid>
      <Grid item>
        <List>
          {listItems.map((listItem,index) => (
            <ListItemButton key={index}
              onClick={() => {return navigate(listItem.link)}}
            >
              <ListItemText primary={listItem.text} className={classes.listItem} />
            </ListItemButton>
          ))}
        </List>
      </Grid>
    </Grid>
  );

  return (
    <>
      <CssBaseline />
      <IconButton className={classes.iconButton} onClick={toggleSlider(!open)} style={{ position: 'absolute', top: 0, left: 0 }}>
        <Menu style={{fontSize:"3rem"}} />
      </IconButton>
      <Drawer open={open} anchor="left" onClose={toggleSlider(false)}>
        <SideList />
      </Drawer>
    </>
  );
}
