import { useState } from "react";
import {
  IconButton,
  List,
  ListItemText,
  CssBaseline,
  Drawer,
  Grid,
  ListItemButton,
} from "@mui/material";
import {
  Menu
} from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

/**
 * Renders the navbar.
 * @returns - A Drawer with a list of navigation items.
 */
export default function Navbar() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const toggleSlider = (openState:boolean) => () => {
    setOpen(openState);
  };
  const { t } = useTranslation();
  const listItems = [
    {link: "/", text: t("homepage")},
    {link: "/projects", text: t("myProjects")},
    {link: "/courses", text: t("myCourses")}
  ]

  const SideList = () => (
    <Grid container direction="column" sx={{
      width: 250,
      background: "#373b42",
      height: "100%"
    }}>
      <Grid item container direction="row" alignItems="flex-start">
        <IconButton onClick={toggleSlider(!open)} sx={{
          color: "blue"
        }}>
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
              <ListItemText primary={listItem.text} sx={{color:"white"}} />
            </ListItemButton>
          ))}
        </List>
      </Grid>
    </Grid>
  );

  return (
    <>
      <CssBaseline />
      <IconButton sx={{color:"blue"}} onClick={toggleSlider(!open)} style={{ position: 'absolute', top: 0, left: 0 }}>
        <Menu style={{fontSize:"3rem"}} />
      </IconButton>
      <Drawer open={open} anchor="left" onClose={toggleSlider(false)}>
        <SideList />
      </Drawer>
    </>
  );
}