import React, { useState } from 'react';
import { Grid, TextField, Button, List, ListItem, ListItemText, Typography, Box } from '@mui/material';

export function CourseForm(): JSX.Element {
  const [courseName, setCourseName] = useState('');
  const [assistants, setAssistants] = useState<string[]>([]);

  const handleAddAssistant = () => {
    setAssistants([...assistants, '']);
  };

  return (
    <Grid container direction={'column'} spacing={2}>
      <Grid item>
        <Grid container direction={'column'} spacing={2} justifyContent="center" alignItems="center" style={{ minHeight: '80vh', maxWidth: '100%' }} >
          <Grid item>
            <Typography variant="h4">Naam Vak</Typography>
          </Grid>
          <Grid item>
            <TextField
              value={courseName}
              onChange={(e) => setCourseName(e.target.value)}
              sx={{ width: '50ch', maxWidth: '100%'}}
            />
          </Grid>
        </Grid>
      </Grid>
      <Grid item container justifyContent="flex-end">
        <Button variant="contained" color="primary" style={{ borderRadius: '50px',paddingLeft:'2rem',paddingRight:'2rem' }}>
          <Typography variant='h5'>Opslaan</Typography>
        </Button>
      </Grid>
    </Grid>
  );
}