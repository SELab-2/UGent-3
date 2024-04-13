import { Button, Card, CardActions, CardContent, CardHeader, Grid, Paper, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Course, Project, apiHost, loggedInToken, getIdFromLink, getNearestFutureDate } from "./CourseUtils";
import { useParams, useNavigate, Link } from "react-router-dom";
import { Title } from "../Header/Title";

interface UserUid{
    uid: string
}

/**
 * 
 * @returns A jsx component representing the course detail page for a teacher
 */
export function CourseDetailTeacher(): JSX.Element {
  const [course, setCourse] = useState<Course>();
  const [projects, setProjects] = useState<Project[]>([]);
  const [admins, setAdmins] = useState<UserUid[]>([]);
  const [students, setStudents] = useState<UserUid[]>([]);
  const { courseId } = useParams<{ courseId: string }>();
  
  const { t } = useTranslation('translation', { keyPrefix: 'courseDetailTeacher' });
  
  const navigate = useNavigate();
  useEffect(() => {
    fetch(`${apiHost}/courses/${courseId}`, {
      headers: {
        "Authorization": loggedInToken()
      }
    })
      .then(response => response.json())
      .then(data => setCourse(data.data))
      .catch(error => console.error('Error:', error));
  }, [courseId]);
    
  useEffect(() => {
    if(courseId){
      const params = new URLSearchParams({ course_id: courseId });
      fetch(`${apiHost}/projects?${params}`, {
        headers: {
          "Authorization": loggedInToken()
        }
      })
        .then(response => response.json())
        .then(data => setProjects(data.data))
        .catch(error => console.error('Error:', error));
    }
  }, [courseId]);
    
  useEffect(() => {
    fetch(`${apiHost}/courses/${courseId}/admins`, {
      headers: {
        "Authorization": loggedInToken()
      }
    })
      .then(response => response.json())
      .then(data => setAdmins(data.data))
      .catch(error => console.error('Error:', error));
  
  }, [courseId]);
  
  useEffect(() => {
    fetch(`${apiHost}/courses/${courseId}/students`, {
      headers: {
        "Authorization": loggedInToken()
      }
    })
      .then(response => response.json())
      .then(data => setStudents(data.data))
      .catch(error => console.error('Error:', error));
  
  }, [courseId]);
    
  if(course == undefined){
    return <><Typography>Loading course page</Typography></>;
  }
  else {
    return (
      <>
        <Title title={t('title')}></Title>
        <Grid container margin={"2rem"} direction={"column"}>
          <Grid item marginBottom={"1rem"}>
            <Typography variant="h4">{course.name}</Typography>
          </Grid>
          <Grid item>
            <Grid container direction={"row"}>
              <Grid item style={{ width: "50%" }}>
                <Paper elevation={0} style={{ border: "1px solid black" }}>
                  <Typography variant="h5">{t('projects')}</Typography>
                  <Grid container direction={"row"}>
                    {projects?.map((project) => (
                      <Grid item margin={"2rem"}>
                        <Card style={{ background: "lightblue" }} key={project.project_id}>
                          <Link to={`/projects/${getIdFromLink(project.project_id)}`}>
                            <CardHeader title={project.title} />
                          </Link>
                          <CardContent>
                            {getNearestFutureDate(project.deadlines) &&
                            (
                              <Typography variant="body1">
                                {`${t('deadline')}: ${getNearestFutureDate(project.deadlines)?.toLocaleDateString()}`}
                              </Typography>
                            )}
                          </CardContent>
                          <CardActions>
                            <Button onClick={() => navigate(`/projects/${project.project_id}`)}>{t('view')}</Button>
                          </CardActions>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </Paper>
              </Grid>
              <Grid item style={{ marginLeft: "1rem" }}>
                <Grid container direction={"column"}>
                  <Grid item height={"35vh"}>
                    <Typography variant="h5">{t('admins')}:</Typography>
                    <Grid container direction={"column"}>
                      {admins.map((admin) => (
                        <Grid item>
                          <Typography variant="body1">{admin.uid}</Typography>
                        </Grid>
                      ))}
                    </Grid>
                  </Grid>
                  <Grid item height={"40vh"}>
                    <Typography variant="h5">{t('students')}:</Typography>
                    <Grid container direction={"column"}>
                      {students.map((student) => (
                        <Grid item>
                          <Typography variant="body1">{student.uid}</Typography>
                        </Grid>
                      ))}
                    </Grid>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </>
    );
  }
}