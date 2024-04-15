import { Button, Card, CardActions, CardContent, CardHeader, Checkbox, Grid, IconButton, Paper, Typography } from "@mui/material";
import { ChangeEvent, useState } from "react";
import { useTranslation } from "react-i18next";
import { Course, Project, apiHost, loggedInToken, getIdFromLink, getNearestFutureDate, getUserName } from "./CourseUtils";
import { Link, useNavigate, NavigateFunction, useLoaderData } from "react-router-dom";
import { Title } from "../Header/Title";
import ClearIcon from '@mui/icons-material/Clear';

interface UserUid{
    uid: string
}

/**
 * Handles the deletion of an admin.
 * @param navigate - The navigate function from react-router-dom.
 * @param courseId - The ID of the course.
 * @param uid - The UID of the admin.
 */
function handleDeleteAdmin(navigate: NavigateFunction, courseId: string, uid: string): void {
  fetch(`${apiHost}/courses/${courseId}/admins`, {
    method: 'DELETE',
    headers: {
      "Authorization": loggedInToken(),
      "Content-Type": "application/json" // Add this line
    },
    body: JSON.stringify({ // Convert the body object to JSON
      "admin_uid": uid
    })
  })
    .then(() => {
      navigate(0);
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Handles the deletion of a student.
 * @param navigate - The navigate function from react-router-dom.
 * @param courseId - The ID of the course.
 * @param uid - The UID of the admin.
 */
function handleDeleteStudent(navigate: NavigateFunction, courseId: string, uids: string[]): void {
  fetch(`${apiHost}/courses/${courseId}/students`, {
    method: 'DELETE',
    headers: {
      "Authorization": loggedInToken(),
      "Content-Type": "application/json" // Add this line
    },
    body: JSON.stringify({ // Convert the body object to JSON
      "students": uids
    })
  })
    .then(() => {
      navigate(0);
    })
    .catch(error => console.error('Error:', error));
}
/**
 * 
 * @returns A jsx component representing the course detail page for a teacher
 */
export function CourseDetailTeacher(): JSX.Element {
  const [selectedStudents, setSelectedStudents] = useState<string[]>([]);

  const courseDetail = useLoaderData() as {
    course: Course ,
    projects:Project[] ,
    admins: UserUid[],
    students: UserUid[]
  };
  const { course, projects, admins, students } = courseDetail;

  const { t } = useTranslation('translation', { keyPrefix: 'courseDetailTeacher' });
  const { i18n } = useTranslation();
  const lang = i18n.language;
  const navigate = useNavigate();

  const handleCheckboxChange = (event: ChangeEvent<HTMLInputElement>, uid: string) => {
    if (event.target.checked) {
      setSelectedStudents((prevSelected) => [...prevSelected, uid]);
    } else {
      setSelectedStudents((prevSelected) =>
        prevSelected.filter((student) => student !== uid)
      );
    }
  };
    
  return (
    <>
      <Title title={t('title')}></Title>
      <Grid container margin={"1rem"} direction={"column"}>
        <Grid item marginBottom={"0.5rem"}>
          <Typography variant="h4">{course.name}</Typography>
        </Grid>
        <Grid item>
          <Grid container direction={"row"}>
            <Grid item style={{ width: "50%" }}>
              <Paper elevation={0} style={{ height:"70vh", maxHeight:"70vh", overflowY:"auto"}}>
                <Typography variant="h5">{t('projects')}:</Typography>
                <Grid container direction={"row"}>
                  {projects?.map((project) => (
                    <Grid item key={project.project_id} margin={"2rem"}>
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
                          <Link to={`/projects/${project.project_id}`}>
                            <Button>{t('view')}</Button>
                          </Link>
                        </CardActions>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
              <Link to={`/${lang}/projects/create?course_id=${course.course_id}`}><Button>{t('newProject')}</Button></Link>
            </Grid>
            <Grid item style={{ marginLeft: "1rem" }}>
              <Grid container direction={"column"}>
                <Grid item position={"relative"} height={"35vh"} width={"35vw"}>
                  <Paper elevation={0} style={{maxHeight:"35vh", overflowY:"auto"}}>
                    <Typography variant="h5">{t('admins')}:</Typography>
                    <Grid container direction={"column"}>
                      {admins.map((admin) => (
                        <Grid item container alignItems="center" spacing={1} key={admin.uid}>
                          <Grid item>
                            <Typography variant="body1">{getUserName(admin.uid)}</Typography>
                          </Grid>
                          <Grid item>
                            <IconButton onClick={() => handleDeleteAdmin(navigate,course.course_id,getIdFromLink(admin.uid))}>
                              <ClearIcon />
                            </IconButton>
                          </Grid>
                        </Grid>
                      ))}
                    </Grid>
                    <Button style={{ position: "absolute", bottom: 0, right: 0 }}>{t('newTeacher')}</Button>
                  </Paper>
                </Grid>
                <Grid item position={"relative"} height={"35vh"} width={"35vw"}>
                  <Typography variant="h5">{t('students')}:</Typography>
                  <Paper elevation={0} style={{maxHeight:"25vh", overflowY:"auto"}}>
                    <Grid container direction="column">
                      {students.map((student) => (
                        <Grid item container alignItems="center" spacing={1} key={student.uid}>
                          <Grid item>
                            <Checkbox
                              checked={selectedStudents.includes(getIdFromLink(student.uid))}
                              onChange={(event) => handleCheckboxChange(event, getIdFromLink(student.uid))}
                            />
                          </Grid>
                          <Grid item>
                            <Typography variant="body1">{getUserName(student.uid)}</Typography>
                          </Grid>
                        </Grid>
                      ))}
                    </Grid>
                  </Paper>
                  <IconButton style={{ position: "absolute", bottom:0, left:0}} onClick={() => handleDeleteStudent(navigate, course.course_id, selectedStudents)}>
                    <ClearIcon />
                    <Typography variant="body1">{t('deleteSelected')}</Typography>
                  </IconButton>
                  <Button style={{ position: "absolute", bottom: 0, right: 0 }}>{t('newStudent')}</Button>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </>
  );

}