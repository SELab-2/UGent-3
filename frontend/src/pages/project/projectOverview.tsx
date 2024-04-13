import {useEffect, useState} from "react";
import {ProjectDeadline} from "./projectDeadline/ProjectDeadline.tsx";
import {fetchProjects} from "./fetchProjects.tsx";
import {Container, Grid, Link, Typography} from "@mui/material";
import {ProjectDeadlineCard} from "./projectDeadline/ProjectDeadlineCard.tsx";
import { useTranslation } from "react-i18next";

/**
 *
 */
export default function ProjectOverView() {
  const {i18n} = useTranslation()
  const [projects, setProjects] = useState<ProjectDeadline[]>([]);
  useEffect(() => {
    fetchProjects(setProjects).then(() => {
      console.log('Projects fetched successfully');
    })
      .catch((error) => {
        console.error('Error fetching projects:', error);
      });
  }, []);
  const projectsByCourse = projects.reduce((acc: {[key: string]: ProjectDeadline[]}, project) => {
    (acc[project.course.course_id] = acc[project.course.course_id] || []).push(project);
    return acc;
  }, {});
  console.log(projectsByCourse)
  return (
    <Container style={{ paddingTop: '50px' }}>
      {Object.entries(projectsByCourse).map(([courseId, courseProjects]) => (
        <Grid container key={courseId} spacing={2}>
          <Grid item xs={12}>
            <Link href={`/${i18n.language}/course/${courseProjects[0].course.course_id}`} style={{color: 'inherit'}}
              sx={{ textDecorationColor: 'currentColor' }}>
              <Typography variant="h6">{courseProjects[0].course.name} {courseProjects[0].course.ufora_id}</Typography>

            </Link>
          </Grid>
          <Grid item xs={12}>
            <ProjectDeadlineCard deadlines={courseProjects} />
          </Grid>
        </Grid>
      ))}
    </Container>
  )
}