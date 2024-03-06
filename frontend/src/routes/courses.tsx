import { useState, useEffect } from 'react';
import { Container, Typography, Grid, Card, CardContent } from "@mui/material";
import { useParams,useNavigate } from 'react-router-dom';
import { authenticated_fetch } from './authenticated_fetch';

interface Course{
    course_id: number,
    name: string,
    teacher:string,
    ufora_id:string,
    url:string
}
interface CourseDetails{
    ufora_id: string,
    teacher: string,
    admins: string[],
    students: string[],
    projects:string[]
}

export function All_courses() {
    const [courses, setCourses] = useState<Course[]>([]);
    const navigate = useNavigate();
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
                                return navigate(`/courses/${course.course_id}`);
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

interface Project {
    project_id: number,
    title: string,
    descriptions: string,
    course_id: number,
    deadline: string,
    archieved: boolean,
    assignment_file: string,
    regex_expressions: string[],
    script_name: string,
    test_path: string,
    visible_for_students: boolean
}

export function Details_course() {//for student
    const { courseId } = useParams<{ courseId: string }>();
    const [course, setCourse] = useState<CourseDetails>();
    const [projects, setProjects] = useState<Project[]>([]);
    //todo: load different page if student or admin

    useEffect(() => {
        authenticated_fetch("http://127.0.0.1:5000/courses/"+courseId)
            .then(response => response.json())
            .then(data => {
                setCourse(data.data);
            })
            .catch(error => console.error('Error:', error));
    }, []);
    
    //fetch the projects
    useEffect(() => {course?.projects.forEach((projectUrl: string) => {
        console.log(projectUrl)
        fetch(projectUrl)
            .then(response => response.json())
            .then(projectData => {
                setProjects(prevProjects => [...prevProjects, projectData.data]);
            })
            .catch(error => console.error('Error:', error));
    })}, [course]);

    //todo: fetch last submission so we can check score
    return (
        <div>
            <Container>
                <Typography variant="h3" display="flex" justifyContent="center">Ufora id: {course?.ufora_id}</Typography>
                {
                    projects.map((project, index) => (
                        <Typography key={index} variant="h5" display="flex" justifyContent="center">Project: {project.title}</Typography>
                    ))
                }
            </Container>
        </div>
    );
}