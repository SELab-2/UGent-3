import {ProjectDeadline} from "./projectDeadline/ProjectDeadline.tsx";
import {Button, Card, CardContent, Container, Grid, Typography, Link} from "@mui/material";
import {ProjectDeadlineCard} from "./projectDeadline/ProjectDeadlineCard.tsx";
import { useTranslation } from "react-i18next";
import {Title} from "../../components/Header/Title.tsx";
import {useLoaderData, Link as RouterLink} from "react-router-dom";
import dayjs from "dayjs";

/**
 * Displays all the projects
 * @returns the project page
 */
export default function ProjectOverView() {
  const {i18n} = useTranslation()
  const { t } = useTranslation('translation', { keyPrefix: 'projectsOverview' });
  const loader = useLoaderData() as {
    projects: ProjectDeadline[],
    me: string
  }
  const projects = loader.projects
  const me = loader.me
  
  const projectReducer = (acc: {[key: string]: ProjectDeadline[]}, project: ProjectDeadline) => {
    (acc[project.course.course_id] = acc[project.course.course_id] || []).push(project);
    return acc;
  }
  const futureProjectsByCourse = projects
    .filter((p) => (p.deadline && dayjs(dayjs()).isBefore(p.deadline)))
    .sort((a, b) => dayjs(a.deadline).diff(dayjs(b.deadline)))
    .reduce(projectReducer, {});
  const pastProjectsByCourse = projects
    .filter((p) => p.deadline && (dayjs()).isAfter(p.deadline))
    .sort((a, b) => dayjs(b.deadline).diff(dayjs(a.deadline)))
    .reduce(projectReducer, {});
  const noDeadlineProject = projects.filter((p) => p.deadline === undefined)
    .reduce(projectReducer,{});
  
  const projectItem = ([index, courseProjects] : [string, ProjectDeadline[]]) =>{
    return (
      <Grid container spacing={2} key={index}>
        <Grid item xs={12}>
          <Link href={`/${i18n.language}/courses/${courseProjects[0].course.course_id}`} style={{color: 'inherit'}}
            underline={'none'}>
            <Typography variant="h6">{courseProjects[0].course.name} {courseProjects[0].course.ufora_id}</Typography>
          </Link>
        </Grid>
        <Grid item xs={8}>
          <ProjectDeadlineCard deadlines={courseProjects} showCourse={false} />
        </Grid>
      </Grid>
    )
  }
  return (
    <Container style={{ paddingTop: '50px' }}>
      <Title title={"Projects Overview"}/>
      <Grid container spacing={2}>
        <Grid item xs={2}>
          {me === 'TEACHER' && (
            <Button component={RouterLink} to={`/${i18n.language}/projects/create`}>{t('new_project')}</Button>
          )}
        </Grid>
        <Grid item xs={5}>
          <Card>
            <CardContent>
              <Typography variant="h5" style={{ color: '#3f51b5' }}>{t("future_deadline")}:</Typography>
              {Object.keys(futureProjectsByCourse).length + Object.keys(noDeadlineProject).length === 0 ? (
                <Typography variant="body1">
                  {t('no_projects')}
                </Typography>
              ) :(
                [...Object.entries(futureProjectsByCourse),
                  ...Object.entries(noDeadlineProject)].map(projectItem)
              )}
            </CardContent>
          </Card>

        </Grid>
        <Grid item xs={5}>
          <Card>
            <CardContent>
              <Typography variant="h5" style={{ color: '#3f51b5' }}>{t("past_deadline")}:</Typography>
              {
                Object.keys(pastProjectsByCourse).length === 0 ? (
                  <Typography variant="body1">
                    {t('no_projects')}
                  </Typography>
                ):(
                  Object.entries(pastProjectsByCourse).map(projectItem)
                )
              }
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}