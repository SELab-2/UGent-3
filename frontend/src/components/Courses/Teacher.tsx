import { Button, Grid, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useParams,Link } from "react-router-dom";

interface Course{
    course_id: number,
    name: string,
    teacher:string,
    ufora_id:string,
    url:string
}

interface Project{
    title: string,
    project_id: number
}

interface UserUid{
  uid: string
}

export function CourseDetailTeacher(): JSX.Element {
  const [course, setCourse] = useState<Course>();
  const [projects, setProjects] = useState<Project[]>([]);
  const [admins, setAdmins] = useState<UserUid[]>([]);
  const [students, setStudents] = useState<UserUid[]>([]);
  const { courseId } = useParams<{ courseId: string }>();

  useEffect(() => {
    fetch("http://127.0.0.1:5000/courses/" + courseId, {
      headers: {
        "Authorization": "teacher1"
      }
    })
      .then(response => response.json())
      .then(data => setCourse(data.data))
      .catch(error => console.error('Error:', error));
  }, [courseId]);
  
  useEffect(() => {
    if(courseId){
      const params = new URLSearchParams({ course_id: courseId });
      fetch("http://127.0.0.1:5000/projects?" + params, {
        headers: {
          "Authorization": "teacher1"
        }
      })
        .then(response => response.json())
        .then(data => setProjects(data.data))
        .catch(error => console.error('Error:', error));
    }
  }, [courseId]);
  
  useEffect(() => {
    fetch("http://127.0.0.1:5000/courses/" + courseId + "/admins", {
      headers: {
        "Authorization": "teacher1"
      }
    })
      .then(response => response.json())
      .then(data => setAdmins(data.data))
      .catch(error => console.error('Error:', error));

  }, [courseId]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000//courses/" + courseId + "/students", {
      headers: {
        "Authorization": "teacher1"
      }
    })
      .then(response => response.json())
      .then(data => setStudents(data.data))
      .catch(error => console.error('Error:', error));

  }, [courseId]);
  
  return (
    <Grid container direction={'row'} spacing={2}>
      <Grid item>
        <Grid container direction={'column'} spacing={2}>
          <Grid item><Typography variant="h4">{course?.name}</Typography></Grid>
          <Grid item><Typography variant="h6">projecten</Typography></Grid>
          {projects.map((project) => (
            <Grid item key={project.project_id}>
              <Typography variant="body1"><Link to={'/projects/'+project.project_id}>{project.title}</Link></Typography>
            </Grid>
          ))}
          <Grid item><Button><Link to={'/projects/create?courseId='+courseId}>New Project</Link></Button></Grid>
        </Grid>
        <Grid container direction={'column'} spacing={2}>
          <Grid item><Typography variant="h6">lijst co-lesgevers/assistenten</Typography></Grid>
          {
            admins.map((admin) => (
              <Grid item key={admin.uid}>
                <Typography variant="body1">{admin.uid}</Typography>
              </Grid>
            ))
          }
          <Grid item><Button>nieuwe lesgever</Button></Grid>
        </Grid>
        <Grid container direction={'column'} spacing={2}>
          <Grid item><Typography variant="h6">lijst studenten</Typography></Grid>
          {
            students.map((student) => (
              <Grid item key={student.uid}>
                <Typography variant="body1">{student.uid}</Typography>
              </Grid>
            ))
          }
          <Grid item><Button>nieuwe student(en)</Button></Grid>
        </Grid>
      </Grid>
    </Grid>
  );
}