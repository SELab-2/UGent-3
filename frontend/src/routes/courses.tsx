import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Button } from "@mui/material";

export default function All_courses() {
    const [courses, setCourses] = useState<string[]>([]);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/courses")
            .then(response => response.json())
            .then(data => setCourses(data.data)) // data.data contains the course URL
            .catch(error => console.error('Error:', error));
    }, []);

    return (
        <div>
            <Container>
                <Typography variant="h1" display="flex" justifyContent="center">Courses</Typography>
                <Typography variant= "h2" display="flex" justifyContent="center">Please select a course for more details</Typography>
                <Box textAlign="center">
                    {courses.map((courseUrl, index) => (
                        <Button key={index} variant="contained" size="large" onClick={() => {
                            window.location.href = courseUrl; // navigate to the course URL when clicked
                        }}>
                            {courseUrl}
                        </Button>
                    ))}
                </Box>
            </Container>
        </div>
    );
}
