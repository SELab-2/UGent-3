import { useState, useEffect } from 'react';
import { Container, Typography, Box, Button, Grid, Card, CardContent } from "@mui/material";

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
                <Grid container spacing={3}>
                    {courses.map((courseUrl, index) => (
                        <Grid item xs={12} sm={6} md={4} key={index}>
                            <Card>
                                <CardContent>
                                    <Button variant="contained" size="large" fullWidth onClick={() => {
                                        window.location.href = courseUrl; // navigate to the course URL when clicked
                                    }}>
                                        {courseUrl}
                                    </Button>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Container>
        </div>
    );
}
