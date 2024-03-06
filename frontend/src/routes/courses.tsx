import { useState, useEffect } from 'react';
import { Container, Typography, Grid, Card, CardContent } from "@mui/material";
import { useParams } from 'react-router-dom';

interface Course{
    course_id: number,
    name: string,
    teacher:string,
    ufora_id:string,
    url:string
}

export default function All_courses() {
    const [courses, setCourses] = useState<Course[]>([]);

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
                    {courses.map((course) => (
                        <Grid item xs={12} sm={6} md={4} key={course.course_id}>
                            <Card onClick={() => {
                                window.location.href += "/"+course.course_id;
                            }} style={{cursor: 'pointer', backgroundColor: 'gray'}}>
                                <CardContent>
                                    <Typography variant="h5">Name: {course.name}</Typography>
                                    <Typography variant="h6">Ufora id: {course.ufora_id}</Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Container>
        </div>
    );
}

export function Details_course() {
    const { courseId } = useParams<{ courseId: string }>();
    const [course, setCourse] = useState<Course>();

    useEffect(() => {
        fetch("http://127.0.0.1:5000/courses/"+courseId)
            .then(response => response.json())
            .then(data => setCourse(data.data))
            .catch(error => console.error('Error:', error));
    }, []);
    return (
        <div>
            <Container>
                <Typography variant="h1" display="flex" justifyContent="center">Course details</Typography>
                
            </Container>
        </div>
    );
}