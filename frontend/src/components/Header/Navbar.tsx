import React, { useState } from "react";
import {
  Avatar,
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

function NavBarItem(link: string, text: string) {
  const navigate = useNavigate();
  const classes = useStyles();

  return (
    <ListItemButton 
      onClick={() => {return navigate(link)}}
    >
      <ListItemText primary={text} className={classes.listItem} />
    </ListItemButton>
  );
}

export default function Navbar() {
  const classes = useStyles();
  const [open, setOpen] = useState(false);

  const isStudent = true;

  const toggleSlider = (openState: boolean) => () => {
    setOpen(openState);
  };

  const listItems = [
    {link: "/", text: "Homepage"},
    {link: "/projects", text: "Mijn projecten"},
    {link: "/courses", text: "Mijn vakken"}
  ]

  if (isStudent) {
    listItems.splice(1, 0, {link: "/scores", text: "Mijn scores"});
  }

  const sideList = () => (
    <Grid container direction="column" className={classes.menuSliderContainer}>
      <Grid item container direction="row" alignItems="flex-start">
        <IconButton onClick={toggleSlider(!open)} className={classes.iconButton}>
          <Menu style={{fontSize:"3rem"}} />
        </IconButton>
        <Avatar
          className={classes.avatar}
          src="https://i.ibb.co/rx5DFbs/avatar.png"
          alt="Juaneme8"
          style={{ margin: "0.5rem 0 0.5rem auto" }}
        />
      </Grid>
      <Grid item>
      </Grid>
      <Grid item>
        <List>
          {listItems.map((listItem) => (
            NavBarItem(listItem.link, listItem.text)
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
        {sideList()}
      </Drawer>
    </>
  );
}
