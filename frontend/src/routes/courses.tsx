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
interface ProjectSubmission {
    project_id: number,
    submission_id: number,
    title: string,
    score: number
}

/**
 * @returns The component to render for all courses in student view.
 */
export function All_courses() {
  const [courses, setCourses] = useState<Course[]>([]);
  const navigate = useNavigate();
  //todo: check if the user is a teacher
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

/**
 * @returns The component to render depending on role of user.
 */
export function Student_or_admin() {
  //send a fetch to courses endpoint to check if uid is admin or student
  //todo: figure out how to get uid
  const is_student = true;
  if (is_student) {
    return <Details_course_student />;
  } else {
    return <Details_course_admin />;
  }
}

/**
 * @returns The component to render of course details for admin.
 */
function Details_course_admin() {//for admin
  
  return (
    <Typography variant="h3" display="flex" justifyContent="center">Under construction</Typography>
  )

}

/**
 * @returns Tje component to render of course details for student.
 */
function Details_course_student() {//for student
  const { courseId } = useParams<{ courseId: string }>();
  const [course, setCourse] = useState<CourseDetails>();
  const [projectSubmissions, setProjectSubmissions] = useState<ProjectSubmission[]>([]);
  //todo: load different page if student or admin
  const navigate = useNavigate();
  useEffect(() => {
    authenticated_fetch("http://127.0.0.1:5000/courses/"+courseId)
      .then(response => response.json())
      .then(data => {
        setCourse(data.data);
      })
      .catch(error => console.error('Error:', error));
  }, [courseId]);
    
  //fetch the projects and submission scores
  useEffect(() => {course?.projects.forEach((projectUrl: string) => {
    fetch(projectUrl)
      .then(response => response.json())
      .then(projectData => {
        const submission = fetch_fake_submission(projectData.data.project_id);
        setProjectSubmissions(prevProjectSubmissions => 
          [...prevProjectSubmissions, {project_id:projectData.data.project_id, submission_id:submission.submission_id, title: projectData.data.title, score: submission.score}]);
      })
      .catch(error => console.error('Error:', error));
  })}, [course]);

  return (
    <Container>
      <Typography variant="h3" display="flex" justifyContent="center">Ufora id: {course?.ufora_id}</Typography>
      <Grid container spacing={3}>
        {projectSubmissions.map((projectSubmission, index) => (
          <Grid item xs={12} key={index}>
            <Grid container justifyContent="space-between">
              <Card onClick={() => {
                return navigate(`/projects/${projectSubmission.project_id}`);
              }} style={{backgroundColor: 'gray'}}>
                <CardContent>
                  <Typography variant="h5">Project: {projectSubmission.title}</Typography>
                </CardContent>
              </Card>
              <Card style={{backgroundColor: 'gray'}}>
                <CardContent>
                  <Typography variant="h5">Score: {projectSubmission.score}</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

/**
 * Fetches a fake submission.
 * @param {number} project_id - The ID of the project.
 * @returns A mock submission object.
 */
function fetch_fake_submission(project_id:number){
  return {
    "submission_id": 1,
    "student_id": 1,
    "project_id": project_id,
    "submission_date": "2021-10-10",
    "score": 10
  }
}
