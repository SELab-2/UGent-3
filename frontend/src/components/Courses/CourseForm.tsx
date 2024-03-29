import React from 'react';
import { useState } from 'react';
import { FormControl, Box, TextField, Button} from '@mui/material';

/**
 * Renders the CourseForm component.
 * @returns JSX.Element representing the CourseForm component.
 */
export function CourseForm(): JSX.Element {
  const [courseName, setCourseName] = useState('');
  const [error, setError] = useState('');

  const apiHost = import.meta.env.VITE_API_HOST;

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCourseName(event.target.value);
    setError(''); // Clearing error message when user starts typing
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevents the default form submission behaviour
    
    if (!courseName.trim()) {
      setError('Course name should not be empty');
      return;
    }

    const data = { name: courseName };
    call_to_api(apiHost + '/courses', JSON.stringify(data), 'POST');
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="center" height="90vh" position="relative">
      <form onSubmit={handleSubmit}>
        <FormControl>
          <TextField
            label="course name"
            value={courseName}
            onChange={handleInputChange}
            error={!!error} // Applying error style if there's an error message
            helperText={error} // Displaying the error message
            sx={{ borderColor: error ? 'red' : undefined }} // Changing border color to red if there's an error
          />
        </FormControl>
        <Button
          type="submit"
          style={{
            position: 'absolute',
            bottom: '15rem',
            right: '30rem',
          }}
        >
          Submit
        </Button>
      </form>
    </Box>
  );
}

/**
 * Helper function to send requests to the a</Button>pi
 * @param path - path to the api 
 * @param data - data to send
 * @param method - POST, PATCH, GET or DELETE
 */
function call_to_api(path: string, data: string, method:string){
  fetch(path, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'teacher1'
    },
    body: data,
  })
    .then(response => response.json())
    .then(data => {
      window.location.href = data.url; // navigate to data.url
    })
    .catch((error) => {
      console.error('Error:', error); //should redirect to error page
    });
}