import { Box, Button, Card, CardActions, CardContent, CardHeader, Dialog, DialogActions, DialogTitle, FormControl, FormLabel, Grid, Paper, TextField, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useParams, useNavigate, NavigateFunction, Link } from "react-router-dom";

interface Course{
    course_id: string,
    name: string,
    teacher:string,
    ufora_id:string,
    url:string
}

interface Project{
    title: string,
    project_id: string,
    deadline: Date
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
  const [courses, setActiveCourses] = useState<Course[]>([]);
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
        setActiveCourses(data.data);
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
    <Grid container direction={'column'} style={{marginTop: '20px'}}>
      <SideScrollableCourses courses={courses}></SideScrollableCourses>
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
      <Grid item style={{marginLeft:"2rem", marginTop:"2rem"}}>
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
 * We should reuse this in the student course view since it will be mainly the same except the create button.
 * @param props - The component props requiring the courses that will be displayed in the scroller.
 * @returns A component to display courses in horizontal scroller where each course is a card containing its name.
 */
function SideScrollableCourses({courses}: {courses: Course[]}): JSX.Element {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [projects, setProjects] = useState<{ [courseId: string]: Project[] }>({});

  useEffect(() => {
    // Fetch projects for each course
    const fetchProjects = async () => {
      const projectPromises = courses.map(course =>
        fetch(`${apiHost}/projects?course_id=${getIdFromLink(course.course_id)}`, 
          { headers: { "Authorization": loggedInToken() } })
          .then(response => response.json())
      );

      const projectResults = await Promise.all(projectPromises);
      const projectsMap: { [courseId: string]: Project[] } = {};

      projectResults.forEach((result, index) => {
        projectsMap[getIdFromLink(courses[index].course_id)] = result.data;
      });

      setProjects(projectsMap);
      console.log(projectsMap);
    };

    fetchProjects();
  }, [courses]);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const filteredCourses = courses.filter(course => 
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Grid item xs={12} marginLeft="2rem">
      <Box display="flex" marginBottom="1rem">
        <TextField
          variant="outlined"
          label="Search"
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </Box>
      <Paper style={{width: '100%', height: '100%', overflowY: 'auto', boxShadow: 'none', display: 'flex', justifyContent: 'center' }}>
        <Grid container direction="row" spacing={5} alignItems="flex-start">
          {filteredCourses.map((course, index) => (
            <Grid item key={index} xs={12} sm={6} md={4} lg={2}>
              <Card variant='outlined'>
                <CardHeader title={<EpsilonTypography text={course.name}/>}/>
                <CardContent style={{margin:"10", height:"12vh"}}>
                  {course.ufora_id && (
                    <EpsilonTypography text={`Ufora_id:${course.ufora_id}`}/>
                  )}
                  <EpsilonTypography text={`Teacher: ${course.teacher}`}/>
                  <Typography variant="body1">Projects:</Typography>
                  {projects[getIdFromLink(course.course_id)] && projects[getIdFromLink(course.course_id)].slice(0, 3).map((project) => (
                    <Grid item key={project.project_id}>
                      <Link to={`/projects/${getIdFromLink(project.project_id)}`}><EpsilonTypography text={`${project.title} ${project.deadline}`}/></Link>
                    </Grid>
                  ))}
                </CardContent>
                <CardActions>
                  <Button onClick={() => navigate(`/courses/${getIdFromLink(course.course_id)}`)}>View</Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Grid>
  );
}

function EpsilonTypography({text} : {text: string}): JSX.Element {
  return (
    <Typography variant="body1" style={{ maxWidth: '13rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{text}</Typography>
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