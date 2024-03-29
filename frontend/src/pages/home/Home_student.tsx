import { useTranslation } from "react-i18next";
import { Card, CardContent, Typography, Grid , Container} from '@mui/material';
import {useEffect } from 'react';

/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function HomeStudent() {
  const { t } = useTranslation();
  useEffect(() => {
    fetch("http://127.0.0.1:5000/project?uid=123")
      .then(response => response.json())
  }, []);
  return (
    <Container style={{ paddingTop: '50px' }}>
      <Grid item>
        <Card>
          <CardContent>
            <Typography variant="body2">
              {t('myProjects')}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
    </Container>
  );
}
