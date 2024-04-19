import { Box, Button, Card, CardActions, CardContent, CardHeader, Grid, Paper, TextField, Typography } from "@mui/material";
import { Course, Project, apiHost, getIdFromLink, getNearestFutureDate } from "./CourseUtils";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect, useMemo } from "react";
import { useTranslation } from "react-i18next";
import debounce from 'debounce';

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
  //const navigate = useNavigate();
  const location = useLocation();
  const navigate = useNavigate();

  // Get initial state from URL
  const urlParams = useMemo(() => new URLSearchParams(location.search), [location.search]); //useMemo so only recompute when location.search changes
  const initialSearchTerm = urlParams.get('name') || '';
  const initialUforaIdFilter = urlParams.get('ufora_id') || '';
  const initialTeacherNameFilter = urlParams.get('teacher') || '';

  const [searchTerm, setSearchTerm] = useState(initialSearchTerm);
  const [uforaIdFilter, setUforaIdFilter] = useState(initialUforaIdFilter);
  const [teacherNameFilter, setTeacherNameFilter] = useState(initialTeacherNameFilter);
  const [projects, setProjects] = useState<{ [courseId: string]: Project[] }>({});

  const debouncedHandleSearchChange = useMemo(() =>
    debounce((key: string, value: string) => {
      if (value === '') {
        urlParams.delete(key);
      } else {
        urlParams.set(key, value);
      }
      const newUrl = `${location.pathname}?${urlParams.toString()}`;
      navigate(newUrl, { replace: true });
    }, 500), [urlParams, navigate, location.pathname]);

  useEffect(() => {
    debouncedHandleSearchChange('name', searchTerm);
  }, [searchTerm, debouncedHandleSearchChange]);

  useEffect(() => {
    debouncedHandleSearchChange('ufora_id', uforaIdFilter);
  }, [uforaIdFilter, debouncedHandleSearchChange]);

  useEffect(() => {
    debouncedHandleSearchChange('teacher', teacherNameFilter);
  }, [teacherNameFilter, debouncedHandleSearchChange]);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newSearchTerm = event.target.value;
    setSearchTerm(newSearchTerm);
  };

  const handleUforaIdFilterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newUforaIdFilter = event.target.value;
    setUforaIdFilter(newUforaIdFilter);
  };

  const handleTeacherNameFilterChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newTeacherNameFilter = event.target.value;
    setTeacherNameFilter(newTeacherNameFilter);
  };

  useEffect(() => {
    // Fetch projects for each course
    const fetchProjects = async () => {
      const projectPromises = courses.map(course =>
        fetch(`${apiHost}/projects?course_id=${getIdFromLink(course.course_id)}`, 
          { credentials: 'include' }
        )
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

  const filteredCourses = courses.filter(course => 
    course.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (course.ufora_id ? course.ufora_id.toLowerCase().includes(uforaIdFilter.toLowerCase()) : !uforaIdFilter) &&
    course.teacher.toLowerCase().includes(teacherNameFilter.toLowerCase())
  );

  return (
    <Grid item xs={12} marginLeft="2rem">
      <Grid container direction="row" spacing={2}>
        <SearchBox label={'name'} searchTerm={searchTerm} handleSearchChange={handleSearchChange}/>
        <SearchBox label={'ufora id'} searchTerm={uforaIdFilter} handleSearchChange={handleUforaIdFilterChange}/>
        <SearchBox label={'teacher'} searchTerm={teacherNameFilter} handleSearchChange={handleTeacherNameFilterChange}/>
      </Grid>
      <EmptyOrNotFilteredCourses filteredCourses={filteredCourses} projects={projects}/>
    </Grid>
  );
}

/**
 * Empty or not. 
 * @returns either a place holder or the actual content.
 */
function EmptyOrNotFilteredCourses({filteredCourses, projects}: {filteredCourses: Course[], projects: { [courseId: string]: Project[] }}): JSX.Element {
  const { t } = useTranslation('translation', { keyPrefix: 'courseDetailTeacher' });
  if(filteredCourses.length === 0){
    return (
      <Typography variant="h5" style={{marginLeft: '2rem'}}>{t('noCoursesFound')}</Typography>
    );
  }

  return (
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
                <EmptyOrNotProjects projects={projects[getIdFromLink(course.course_id)]} noProjectsText={t('noProjects')} />
              </CardContent>
              <CardActions>
                <Link to={`${getIdFromLink(course.course_id)}`}><Button>{t('view')}</Button></Link>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
}
/**
 * @param projects - The projects to be displayed if not empty 
 * @returns either a place holder with text for no projects or the projects
 */
function EmptyOrNotProjects({projects, noProjectsText}: {projects: Project[], noProjectsText:string}): JSX.Element {
  if(projects === undefined || projects.length === 0){
    return (
      <Typography variant="body2" style={{marginLeft: '1rem', marginTop: '0.5rem'}}>{noProjectsText}</Typography>
    );
  }
  else{
    const now = new Date();
    return (
      <>
        {projects.slice(0, 3).map((project) => {
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
      </>
    );
  }
}