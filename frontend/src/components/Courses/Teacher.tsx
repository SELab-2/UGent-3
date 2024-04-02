import { Button, Card, Grid, Paper, Typography } from "@mui/material";
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

  useEffect(() => {
    fetch(`${apiHost}/courses/${courseId}`, {
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
      fetch(`${apiHost}/projects?${params}`, {
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
    fetch(`${apiHost}/courses/${courseId}/admins`, {
      headers: {
        "Authorization": "teacher1"
      }
    })
      .then(response => response.json())
      .then(data => setAdmins(data.data))
      .catch(error => console.error('Error:', error));

  }, [courseId]);

  useEffect(() => {
    fetch(`${apiHost}/courses/${courseId}/students`, {
      headers: {
        "Authorization": "teacher1"
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
                <Typography variant="h6">projecten</Typography>
              </Grid>
              <VerticaleScroller items={projects.map((project) => (
                <Grid item key={project.project_id}>
                  <Typography variant="body1">
                    <Link to={`/projects/${project.project_id}`}>{project.title}</Link>
                  </Typography>
                </Grid>
              ))}></VerticaleScroller>
              <Grid item style={{ alignSelf: 'flex-end' }}>
                <Button>
                  <Link to={`/projects/create?courseId=${courseId}`}>New Project</Link>
                </Button>
              </Grid>
            </Grid>
          </Grid>
          <Grid item>
            <Grid container direction="column" spacing={2}>
              <Grid item>
                <Typography variant="h6">lijst co-lesgevers/assistenten</Typography>
              </Grid>
              <VerticaleScroller items={admins.map((admin) => (
                <Grid item key={admin.uid}>
                  <Typography variant="body1">{admin.uid}</Typography>
                </Grid>
              ))}></VerticaleScroller>
              <Grid item>
                <Button>nieuwe lesgever</Button>
              </Grid>
            </Grid>
          </Grid>
          <Grid item>
            <Grid container direction="column" spacing={2}>
              <Grid item>
                <Typography variant="h6">lijst studenten</Typography>
              </Grid>
              <VerticaleScroller items={students.map((student) => (
                <Grid item key={student.uid}>
                  <Typography variant="body1">{student.uid}</Typography>
                </Grid>
              ))}></VerticaleScroller>
              <Grid item>
                <Button>nieuwe student(en)</Button>
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

  useEffect(() => {
    const params = new URLSearchParams({ teacher: "teacher1" });
    fetch(`${apiHost}/courses?${params}`, {
      headers: {
        "Authorization": "teacher1"
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

  return (
    <Grid container direction={'column'}>
      <SideScrollableCourses courses={activeCourses} title="Active Courses"></SideScrollableCourses>
      <SideScrollableCourses courses={archivedCourses} title="Archived Courses"></SideScrollableCourses>
    </Grid>
  );
}

/**
 * @param props - The component props requiring the courses and title that will be displayed in the scroller.
 * @returns A component to display courses in horizontal scroller where each course is a card containing its name.
 */
function SideScrollableCourses({courses, title}: {courses: Course[], title: string}): JSX.Element {
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
                courses.map((course) => (
                  <Grid item>
                    <Card style={{width: '250px', height: '150px'}}>
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