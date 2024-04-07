import { useTranslation } from "react-i18next";
import { Button, Container, Typography, Box } from "@mui/material";
import {Link } from "react-router-dom";

/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function Home() {
  const { t } = useTranslation('translation', { keyPrefix: 'home' });
  //console.log("log env", process.env.REACT_APP_LOGIN_LINK)
  const login_redirect:string =import.meta.env.VITE_LOGIN_LINK
  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          textAlign: 'center',
          gap: 3,
        }}
      >
        <Box   component="img"src="/logo_ugent.png" alt="University Logo"
          sx={{ width: 100, height: 100 }} />

        <Typography variant="h2" component="h1" gutterBottom  >
          <Box
            component="img"
            src="/logo_app.png"
            alt="University Logo"
            sx={{
              position: 'relative',
              top: '14px',
              width: 90,
              height: 90,
            }}
          />
          Peristerónas
        </Typography>
        <Typography variant="h6" component="p" >
          {t('welcomeDescription', 'Welcome to Peristeronas.')}
        </Typography>
        <Button variant="contained" color="primary" size="large" component={Link} to={login_redirect}>
          {t('login', 'Login')}
        </Button>
      </Box>
    </Container>  );
}
