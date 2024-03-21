import { Grid, Typography } from "@mui/material";
import { Image } from "mui-image"; 
import { useTranslation } from "react-i18next";

/**
 * This component will be rendered when an error occurs.
 * @returns - The ErrorPage component
 */
export function ErrorPage(
  { statusCode, statusTitle, message }: { statusCode: string, statusTitle: string, message: string}
): JSX.Element {

  const { t } = useTranslation();

  return (
    <Grid
      container
      justifyContent="center"
      alignItems="center"
      direction="column"
      sx={{ minHeight: "100vh" }}
      spacing={2}
    >
      <Grid item>
        <Grid
          container
          justifyContent="center"
          alignItems="center"
          spacing={4}
        >
          <Grid item>
            <Typography variant="h1">
              { statusCode }
            </Typography>
          </Grid>
          <Grid item>
            <Image src="/error_pigeon.png" height="20vh" alt="icon" />
          </Grid>
        </Grid>
      </Grid>
      <Grid item>
        <Typography variant="h3">
          { statusTitle }
        </Typography>
      </Grid>
      <Grid item>
        <Typography variant="body1">
          { t(message) }
        </Typography>
      </Grid>
    </Grid>
  );
}
