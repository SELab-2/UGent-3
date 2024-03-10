import {
  AppBar,
  Box,
  Button,
  Toolbar,
  Typography
} from "@mui/material";
import Navbar from "./Navbar";

/**
 * The header component for the application that will be rendered at the top of the page.
 * @returns - The header component
 */
export function Header(): JSX.Element {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="sticky">
        <Toolbar>
          <Box sx={{ flexGrow: 1 }}>
            <Navbar />
          </Box>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Home
          </Typography>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
