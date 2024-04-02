import { Button, Card, Dialog, DialogActions, DialogTitle, FormControl, FormLabel, Grid, Paper, TextField, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams, useNavigate, NavigateFunction } from "react-router-dom";

interface Course{
    course_id: string,
    name: string,
    teacher:string,
    ufora_id:string,
    url:string
}

interface Project{
    title: string,
    project_id: string
}

interface UserUid{
  uid: string
}

/**
 * @returns The uid of the acces token of the logged in user
 */
function loggedInToken(){
  return "teacher1";
}

/**
 * @returns The Uid of the logged in user
 */
function loggedInUid(){
  return "Gunnar";
}

const apiHost = import.meta.env.VITE_API_HOST;
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
  
  return (
    <Grid container direction="column" spacing={2}>
      <Grid item>
        <Typography variant="h4">{course?.name}</Typography>
      </Grid>
      <Grid item>
        <Grid container direction="row" justifyContent="space-between" alignItems="flex-start">
          <Grid item>
            <Grid container direction="column" spacing={2} style={{ minHeight: '100vh' }}>
              <Grid item>
                <Typography variant="h6">{t('projects')}</Typography>
              </Grid>
              <VerticaleScroller items={projects.map((project) => (
                <Grid item key={project.project_id}>
                  <Typography variant="body1" onClick={() => navigate(`/projects/${getIdFromLink(project.project_id)}`)} paragraph component="span">
                    {project.title}
                  </Typography>
                </Grid>
              ))}></VerticaleScroller>
              <Grid item style={{ alignSelf: 'flex-end' }}>
                <Button onClick={() => navigate(`/projects/create?courseId=${courseId}`)}>
                  {t('newProject')}
                </Button>
              </Grid>
            </Grid>
          </Grid>
          <Grid item>
            <Grid container direction="column" spacing={2}>
              <Grid item>
                <Typography variant="h6">{t('assistantList')}</Typography>
              </Grid>
              <VerticaleScroller items={admins.map((admin) => (
                <Grid item key={admin.uid}>
                  <Typography variant="body1">{admin.uid}</Typography>
                </Grid>
              ))}></VerticaleScroller>
              <Grid item>
                <Button>{t('newTeacher')}</Button>
              </Grid>
            </Grid>
          </Grid>
          <Grid item>
            <Grid container direction="column" spacing={2}>
              <Grid item>
                <Typography variant="h6">{t('studentList')}</Typography>
              </Grid>
              <VerticaleScroller items={students.map((student) => (
                <Grid item key={student.uid}>
                  <Typography variant="body1">{student.uid}</Typography>
                </Grid>
              ))}></VerticaleScroller>
              <Grid item>
                <Button>{t('newStudent')}</Button>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
}

/**
 * Renders a vertical scroller component.
 * @param props - The component props requiring the items that will be displayed in the scroller.
 * @returns The rendered vertical scroller component.
 */
function VerticaleScroller({items}: {items: JSX.Element[]}): JSX.Element {
  return (
    <Grid item>
      <Paper style={{maxWidth:"100%", maxHeight:600,height:600, overflowY: 'auto' }}>
        <Grid container direction="column">
          {items}
        </Grid>
      </Paper>
    </Grid>
  );
}

/**
 * @returns A jsx component representing all courses for a teacher
 */
export function AllCoursesTeacher(): JSX.Element {
  const [activeCourses, setActiveCourses] = useState<Course[]>([]);
  const [archivedCourses, setArchivedCourses] = useState<Course[]>([]);
  const [open, setOpen] = useState(false);

  const [courseName, setCourseName] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const { t } = useTranslation('translation', { keyPrefix: 'allCoursesTeacher' });

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  useEffect(() => {
    const params = new URLSearchParams({ teacher: loggedInUid() });
    fetch(`${apiHost}/courses?${params}`, {
      headers: {
        "Authorization": loggedInToken()
      }
    })
      .then(response => response.json())
      .then(data => {
        //const active = data.data.filter((course: Course) => !course.archived);
        //const archived = data.data.filter((course: Course) => course.archived);
        //setActiveCourses(active);
        //setArchivedCourses(archived);
        setActiveCourses(data.data);//TODO change once courses can be archiveable
        setArchivedCourses([]);
      })
      .catch(error => console.error('Error:', error));
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCourseName(event.target.value);
    setError(''); // Clearing error message when user starts typing
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevents the default form submission behaviour

    if (!courseName.trim()) {
      setError(t('emptyCourseNameError'));
      return;
    }

    const data = { name: courseName };
    callToApi(`${apiHost}/courses`, JSON.stringify(data), 'POST', navigate);
  };

  return (
    <Grid container direction={'column'} style={{marginTop: '20px', marginLeft: '20px'}}>
      <SideScrollableCourses courses={activeCourses} title={t("activeCourses")}></SideScrollableCourses>
      <SideScrollableCourses courses={archivedCourses} title={t("archivedCourses")}></SideScrollableCourses>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{t('courseForm')}</DialogTitle>
        <form onSubmit={handleSubmit}>
          <FormControl>
            <FormLabel htmlFor="course-name">{t('courseName')}</FormLabel>
            <TextField
              value={courseName}
              onChange={handleInputChange}
              error={!!error} // Applying error style if there's an error message
              helperText={error} // Displaying the error message
              sx={{ borderColor: error ? 'red' : undefined }} // Changing border color to red if there's an error
            />
          </FormControl>
          <DialogActions>
            <Button onClick={handleClose}>{t('cancel')}</Button>
            <Button type="submit">{t('submit')}</Button>
          </DialogActions>
        </form>
      </Dialog>
      <Grid item style={{marginLeft:'500px'}}>
        <Button onClick={handleClickOpen} >{t('create')}</Button>
      </Grid>
    </Grid>
  );
}

/**
 * 
 * @param path - path to backend api endpoint
 * @param data - optional data to send to the api
 * @param method - POST, GET, PATCH, DELETE
 * @param navigate - function that allows the app to redirect
 */
function callToApi(path: string, data: string, method:string, navigate: NavigateFunction){
  
  fetch(path, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': loggedInToken()
    },
    body: data,
  })
    .then(response => response.json())
    .then(data => {
      navigate(getIdFromLink(data.url)); // navigate to data.url
    })
    .catch((error) => {
      console.error('Error:', error); //should redirect to error page
    });
}

/**
 * @param props - The component props requiring the courses and title that will be displayed in the scroller.
 * @returns A component to display courses in horizontal scroller where each course is a card containing its name.
 */
function SideScrollableCourses({courses, title}: {courses: Course[], title: string}): JSX.Element {
  const navigate = useNavigate();
  return (
    <Grid item>
      <Grid container direction="column">
        <Grid item>
          <Typography variant="h4">{title}</Typography>
        </Grid>
        <Grid item>
          <Paper style={{maxWidth:600,width:600,height:300,overflowX:'auto', boxShadow: 'none', display: 'flex', justifyContent: 'center'}}>
            <Grid container direction="row" spacing={5} alignItems="center">
              {
                courses.map((course, index) => (
                  <Grid item key={index}>
                    <Card style={{width: '250px', height: '150px'}} onClick={() => navigate(getIdFromLink(course.course_id))}>
                      <Typography variant="h6">{course.name}</Typography>
                    </Card>
                  </Grid>
                ))
              }
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Grid>
  );
}

/**
 * @param link - the link to the api endpoint
 * @returns the Id at the end of the link
 */
function getIdFromLink(link: string): string {
  const parts = link.split('/');
  return parts[parts.length - 1];
}