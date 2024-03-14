import { Box, Typography } from "@mui/material";

/**
 * This component is the ServerError component that will be rendered when a general server error occurs.
 * @returns - The ServerError component
 */
export function ServerError() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h1">
        5XX
      </Typography>
      <Typography variant="h3">
        General Server Error
      </Typography>
      <Typography variant="body1">
        Sorry, there seems to be a problem with the server.  
      </Typography>
      <Box component="img" src="/error_pigeon.png" alt="icon" />
    </Box>
  );
}