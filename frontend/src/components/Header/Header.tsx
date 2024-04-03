import {
  AppBar,
  Box,
  Button,
  IconButton,
  Toolbar,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

interface Props {
  // value of the header
  headerText?: string;
}

/**
 * The header component for the application that will be rendered at the top of the page.
 * @param props - React props
 * @returns The header component.
 */
export function Header({ headerText }: Props): JSX.Element {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="sticky">
        <Toolbar>
          <IconButton size="large" color="inherit">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {headerText}
          </Typography>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
