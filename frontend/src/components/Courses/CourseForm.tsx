import React, { useState } from 'react';
import { Grid, TextField, Button, List, ListItem, ListItemText, Typography } from '@mui/material';

export function CourseForm(): JSX.Element {
  const [courseName, setCourseName] = useState('');
  const [assistants, setAssistants] = useState<string[]>([]);

  const handleAddAssistant = () => {
    setAssistants([...assistants, '']);
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <Grid container direction={'column'} spacing={2} justifyContent="center" alignItems="center" style={{ minHeight: '100vh' }} >
          <Grid item>
            <Typography variant="h4">Naam Vak</Typography>
          </Grid>
          <Grid item>
            <TextField
              value={courseName}
              onChange={(e) => setCourseName(e.target.value)}
              sx={{ width: '50ch'}}
            />
          </Grid>
        </Grid>
      </Grid>
      <Grid item xs={6}>
        <List>
          {assistants.map((assistant, index) => (
            <ListItem key={index}>
              <ListItemText primary={`Assistant ${index + 1}`} />
            </ListItem>
          ))}
        </List>
        <Button onClick={handleAddAssistant}>Add Assistant</Button>
      </Grid>
    </Grid>
  );
}