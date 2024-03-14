import { Box, Typography } from "@mui/material";

/**
 * This component is the NotFound component that will be rendered when a page is not found.
 * @returns - The NotFound component
 */
export function NotFound() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h1">
        404
      </Typography>
      <Typography variant="h3">
        Page Not Found
      </Typography>
      <Typography variant="body1">
        Sorry, the page you are looking for could not be found.  
      </Typography>
      <Box component="img" src="/error_pigeon.png" alt="icon" />
    </Box>
  );
}