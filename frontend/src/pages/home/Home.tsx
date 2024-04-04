import { useTranslation } from "react-i18next";
import { Button, Container, Typography, Box } from "@mui/material";


/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function Home() {
  const { t } = useTranslation('translation', { keyPrefix: 'home' });
  const handleLoginClick = () => {
    // Handle login button click here
  };
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

        <Typography variant="h2" component="h1" gutterBottom>
          Peristeronas
        </Typography>
        <Typography variant="h6" component="p">
          {t('welcomeDescription', 'Welcome to Peristeronas.')}
        </Typography>
        <Button variant="contained" color="primary" size="large" onClick={handleLoginClick}>
          {t('login', 'Login')}
        </Button>
      </Box>
    </Container>  );
}
