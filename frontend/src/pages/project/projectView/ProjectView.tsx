import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Container,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import {useLocation, useParams} from "react-router-dom";
import SubmissionCard from "./SubmissionCard";
import { Course } from "../../../types/course";
import { Title } from "../../../components/Header/Title";
import { authenticatedFetch } from "../../../utils/authenticated-fetch";
import i18next from "i18next";
import {useTranslation} from "react-i18next";

const API_URL = import.meta.env.VITE_APP_API_HOST;

interface Project {
  title: string;
  description: string;
  regex_expressions: string[];
}

/**
 *
 * @returns - ProjectView component which displays the project details
 * and submissions of the current user for that project
 */
export default function ProjectView() {

  const location = useLocation();

  const { t } = useTranslation('translation', { keyPrefix: 'projectView' });

  const { projectId } = useParams<{ projectId: string }>();
  const [projectData, setProjectData] = useState<Project | null>(null);
  const [courseData, setCourseData] = useState<Course | null>(null);
  const [assignmentRawText, setAssignmentRawText] = useState<string>("");

  useEffect(() => {
    authenticatedFetch(`${API_URL}/projects/${projectId}`).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          const projectData = data["data"];
          setProjectData(projectData);
          authenticatedFetch(
            `${API_URL}/courses/${projectData.course_id}`
          ).then((response) => {
            if (response.ok) {
              response.json().then((data) => {
                setCourseData(data["data"]);
              });
            }
          });
        });
      }
    });

    authenticatedFetch(
      `${API_URL}/projects/${projectId}/assignment?lang=${i18next.resolvedLanguage}`
    ).then((response) => {
      if (response.ok) {
        response.text().then((data) => setAssignmentRawText(data));
      }
    });
  }, [projectId]);

  if (!projectId) return null;

  return (
    <Grid
      width="100%"
      container
      direction="column"
      rowGap="2rem"
      margin="2rem 0"
    >
      <Grid item sm={12}>
        <Container>
          {projectData && (
            <Card>
              <Title title={projectData.title} />
              <CardHeader
                color="secondary"
                title={projectData.title}
                subheader={
                  <>
                    <Stack direction="row" spacing={2}>
                      <Typography>{projectData.description}</Typography>
                      <Typography flex="1" />
                      {courseData && (
                        <Button variant="contained" href={`/${i18next.resolvedLanguage}/courses/${courseData.course_id}`}>
                          {courseData.name}
                        </Button>
                      )}
                    </Stack>
                  </>
                }
              />
              <CardContent>
                <Markdown>{assignmentRawText}</Markdown>
              </CardContent>
            </Card>
          )}
        </Container>
      </Grid>
      <Grid item sm={12}>
        <Container>
          <SubmissionCard
            regexRequirements={projectData ? projectData.regex_expressions : []}
            submissionUrl={`${API_URL}/submissions`}
            projectId={projectId}
          />
        </Container>
      </Grid>
      <Grid item sm={12}>
        <Container>
          <Box sx={{
            display: 'flex',
            justifyContent: 'flex-end',
            p: 1,
            m: 1,
            width: '100%'
          }}>
            <Button sx={{marginRight: "30px"}} variant="contained" href={location.pathname+"/overview"}>{t("projectOverview")}</Button>
          </Box>
        </Container>
      </Grid>
    </Grid>
  );
}
