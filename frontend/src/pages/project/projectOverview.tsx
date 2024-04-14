import {useEffect, useState} from "react";
import {ProjectDeadline} from "./projectDeadline/ProjectDeadline.tsx";
import {fetchProjects} from "./fetchProjects.tsx";
import {Container, Grid, Link, Typography} from "@mui/material";
import {ProjectDeadlineCard} from "./projectDeadline/ProjectDeadlineCard.tsx";
import { useTranslation } from "react-i18next";
import {Title} from "../../components/Header/Title.tsx";

/**
 *
 */
export default function ProjectOverView() {
  const {i18n} = useTranslation()
  const { t } = useTranslation('translation', { keyPrefix: 'projectsOverview' });
  const [projects, setProjects] = useState<ProjectDeadline[]>([]);
  useEffect(() => {
    fetchProjects(setProjects).then(() => {})
      .catch((error) => {
        console.error('Error fetching projects:', error);
      });
  }, []);
  const currentDate = new Date();

  const futureProjectsByCourse = projects
    .filter((p) => new Date(p.deadline) >= currentDate)
    .sort((a, b) =>
      new Date(a.deadline).getTime() - new Date(b.deadline).getTime())
    .reduce((acc: {[key: string]: ProjectDeadline[]}, project) => {
      (acc[project.course.course_id] = acc[project.course.course_id] || []).push(project);
      return acc;
    }, {});
  const pastProjectsByCourse = projects
    .filter((p) => new Date(p.deadline) < currentDate)
    .sort((a, b) =>
      new Date(b.deadline).getTime() - new Date(a.deadline).getTime())
    .reduce((acc: {[key: string]: ProjectDeadline[]}, project) => {
      (acc[project.course.course_id] = acc[project.course.course_id] || []).push(project);
      return acc;
    }, {});

  return (
    <Container style={{ paddingTop: '50px' }}>
      <Title title={"Projects Overview"}/>
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Typography variant="h5" style={{ color: '#3f51b5' }}>{t("future_deadline")}:</Typography>
          {Object.entries(futureProjectsByCourse).map(([index, courseProjects]) => (
            <Grid container spacing={2} key={index}>
              <Grid item xs={12}>
                <Link href={`/${i18n.language}/course/${courseProjects[0].course.course_id}`} style={{color: 'inherit'}}
                  underline={'none'}>
                  <Typography variant="h6">{courseProjects[0].course.name} {courseProjects[0].course.ufora_id}</Typography>
                </Link>
              </Grid>
              <Grid item xs={8}>
                <ProjectDeadlineCard deadlines={courseProjects} />
              </Grid>
            </Grid>
          ))}
        </Grid>
        <Grid item xs={6}>
          <Typography variant="h5" style={{ color: '#3f51b5' }}>{t("past_deadline")}:</Typography>
          {Object.entries(pastProjectsByCourse).map(([index, courseProjects]) => (
            <Grid container spacing={2} key={index}>
              <Grid item xs={12}>
                <Link href={`/${i18n.language}/course/${courseProjects[0].course.course_id}`} style={{color: 'inherit'}}
                  underline={'none'}>
                  <Typography variant="h6">{courseProjects[0].course.name} {courseProjects[0].course.ufora_id}</Typography>
                </Link>
              </Grid>
              <Grid item xs={8}>
                <ProjectDeadlineCard deadlines={courseProjects} />
              </Grid>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </Container>
  )
}