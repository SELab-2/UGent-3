import { useState } from 'react';
import { Grid, TextField, Button, Typography} from '@mui/material';

/**
 * Renders the CourseForm component.
 * @returns JSX.Element representing the CourseForm component.
 */
export function CourseForm(): JSX.Element {
  const [courseName, setCourseName] = useState('');

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
        <Button variant="contained" color="primary" style={{ borderRadius: '50px',paddingLeft:'2rem',paddingRight:'2rem' }}
          onClick={() => {
            fetch('http://127.0.0.1:5000/courses', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': 'teacher1'
              },
              body: JSON.stringify({ name: courseName }),
            })
              .then(response => response.json())
              .then(data => {
                window.location.href = data.url; // navigate to data.url
              })
              .catch((error) => {
                console.error('Error:', error); //should redirect to error page
              });
          }}>
          <Typography variant='h5'>Opslaan</Typography>
        </Button>
      </Grid>
    </Grid>
  );
}