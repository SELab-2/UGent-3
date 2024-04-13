import { Box, Button, Card, CardActions, CardContent, CardHeader, Grid, Paper, TextField, Typography } from "@mui/material";
import { Course, Project, apiHost, getIdFromLink, getNearestFutureDate, loggedInToken } from "./CourseUtils";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
/**
 * @param text - The text to be displayed
 * @returns Typography that overflow into ... when text is too long
 */
export function EpsilonTypography({text} : {text: string}): JSX.Element {
  return (
    <Typography variant="body1" style={{ maxWidth: '13rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{text}</Typography>
  );
}

/**
 * @param label - The label of the search box
 * @param searchTerm - The current search term
 * @param handleSearchChange - The function to handle search term changes
 * @returns a Grid item containing a TextField, used for searching/filtering
 */
export function SearchBox({label,searchTerm,handleSearchChange}: {label: string, searchTerm: string, handleSearchChange: (event: React.ChangeEvent<HTMLInputElement>) => void}): JSX.Element {
  return (
    <Grid item>
      <Box display="flex" marginBottom="1rem">
        <TextField
          variant="outlined"
          label={label}
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </Box>
    </Grid>
  );
}

/**
 * We should reuse this in the student course view since it will be mainly the same except the create button.
 * @param props - The component props requiring the courses that will be displayed in the scroller.
 * @returns A component to display courses in horizontal scroller where each course is a card containing its name.
 */
export function SideScrollableCourses({courses}: {courses: Course[]}): JSX.Element {
  const [searchTerm, setSearchTerm] = useState('');
  const [projects, setProjects] = useState<{ [courseId: string]: Project[] }>({});
  const [uforaIdFilter, setUforaIdFilter] = useState('');
  const [teacherNameFilter, setTeacherNameFilter] = useState('');

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
    };

    fetchProjects();
  }, [courses]);
  const { t } = useTranslation('translation', { keyPrefix: 'courseDetailTeacher' });
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const handleUforaIdFilterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUforaIdFilter(event.target.value);
  };

  const handleTeacherNameFilterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setTeacherNameFilter(event.target.value);
  };

  const filteredCourses = courses.filter(course => 
    course.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (course.ufora_id ? course.ufora_id.toLowerCase().includes(uforaIdFilter.toLowerCase()) : !uforaIdFilter) &&
    course.teacher.toLowerCase().includes(teacherNameFilter.toLowerCase())
  );

  const now = new Date();

  return (
    <Grid item xs={12} marginLeft="2rem">
      <Grid container direction="row" spacing={2}>
        <SearchBox label={'name'} searchTerm={searchTerm} handleSearchChange={handleSearchChange}/>
        <SearchBox label={'ufora id'} searchTerm={uforaIdFilter} handleSearchChange={handleUforaIdFilterChange}/>
        <SearchBox label={'teacher'} searchTerm={teacherNameFilter} handleSearchChange={handleTeacherNameFilterChange}/>
      </Grid>
      <Paper style={{width: '100%', height: '100%', maxHeight:'65vh', overflowY: 'auto', boxShadow: 'none', display: 'flex', justifyContent: 'center' }}>
        <Grid container direction="row" spacing={5} alignItems="flex-start">
          {filteredCourses.map((course, index) => (
            <Grid item key={index} xs={12} sm={6} md={4} lg={2}>
              <Card variant='outlined' style={{width: '14vw'}}>
                <CardHeader title={<EpsilonTypography text={course.name}/>}/>
                <CardHeader subheader={
                  <>
                    {course.ufora_id && (
                      <>
                      Ufora_id: {course.ufora_id}<br />
                      </>
                    )}
                  Teacher: {course.teacher}
                  </>
                }/>
                <CardContent style={{margin:"0.5rem", height:"12vh"}}>
                  <Typography variant="body1">{t('projects')}:</Typography>
                  {projects[getIdFromLink(course.course_id)] && projects[getIdFromLink(course.course_id)].slice(0, 3).map((project) => {
                    let timeLeft = '';
                    if (project.deadlines != undefined) {
                      const deadlineDate = getNearestFutureDate(project.deadlines);
                      if(deadlineDate == null){
                        return <></>
                      }
                      const diffTime = Math.abs(deadlineDate.getTime() - now.getTime());
                      const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));
                      const diffDays = Math.ceil(diffHours * 24);
                      
                      timeLeft = diffDays > 1 ? `${diffDays} days` : `${diffHours} hours`;
                    }
                    return (
                      <Grid item key={project.project_id}>
                        <Link to={`/projects/${getIdFromLink(project.project_id)}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                          <EpsilonTypography text={`${project.title} ${timeLeft ? ` - ${timeLeft}` : ''}`}/>
                        </Link>
                      </Grid>
                    );
                  })}
                </CardContent>
                <CardActions>
                  <Link to={`${getIdFromLink(course.course_id)}`}><Button>{t('view')}</Button></Link>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Grid>
  );
}