import { useTranslation } from "react-i18next";
import { Container, Typography, Box } from "@mui/material";
import { LoginButton } from "../../components/Header/Login.tsx";

/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function Home() {
  const { t } = useTranslation("translation", { keyPrefix: "home" });
  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          textAlign: "center",
          gap: 3,
        }}
      >
        <Box
          component="img"
          src="/img/logo_ugent.png"
          alt="University Logo"
          sx={{ width: 100, height: 100 }}
        />

        <Typography variant="h2" component="h1" gutterBottom>
          <Box
            component="img"
            src="/img/logo_app.png"
            alt="University Logo"
            sx={{
              position: "relative",
              top: "14px",
              width: 90,
              height: 90,
            }}
          />
          Peristerónas
        </Typography>
        <Typography variant="h6" component="p">
          {t("welcomeDescription", "Welcome to Peristeronas.")}
        </Typography>
        <LoginButton />
      </Box>
    </Container>
  );
}
