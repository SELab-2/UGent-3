import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Container,
  Fade,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import SubmissionCard from "./SubmissionCard";
import { Course } from "../../../types/course";
import { Title } from "../../../components/Header/Title";
import { authenticatedFetch } from "../../../utils/authenticated-fetch";
import i18next from "i18next";
import {useTranslation} from "react-i18next";
import {Me} from "../../../types/me.ts";
import {fetchMe} from "../../../utils/fetches/FetchMe.ts";
import DeadlineGrid from "../../../components/DeadlineView/DeadlineGrid.tsx";
import {Deadline} from "../../../types/deadline.ts";

const API_URL = import.meta.env.VITE_APP_API_HOST;

interface Project {
  title: string;
  description: string;
  regex_expressions: string[];
  archived: string;
}

/**
 *
 * @returns - ProjectView component which displays the project details
 * and submissions of the current user for that project
 */
export default function ProjectView() {

  const location = useLocation();
  const [me, setMe] = useState<Me | null>(null);

  const { t } = useTranslation('translation', { keyPrefix: 'projectView' });

  const { projectId } = useParams<{ projectId: string }>();
  const [projectData, setProjectData] = useState<Project | null>(null);
  const [courseData, setCourseData] = useState<Course | null>(null);
  const [assignmentRawText, setAssignmentRawText] = useState<string>("");
  const [deadlines, setDeadlines] = useState<Deadline[]>([]);
  const [alertVisibility, setAlertVisibility] = useState(false)

  const navigate = useNavigate()
  const deleteProject = () => {
    authenticatedFetch(`${API_URL}/projects/${projectId}`, {
      method: "DELETE"
    });
    navigate('/projects');
  }

  const updateProject = async () => {
    authenticatedFetch(`${API_URL}/projects/${projectId}`).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          const projectData = data["data"];
          setProjectData(projectData);

          const transformedDeadlines = projectData.deadlines.map((deadlineArray: string[]): Deadline => ({
            description: deadlineArray[0],
            deadline: deadlineArray[1]
          }));

          setDeadlines(transformedDeadlines);

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
  }

  const archiveProject = async () => {
    const newArchived = !projectData.archived;
    const formData = new FormData();
    formData.append('archived', newArchived.toString());

    await authenticatedFetch(`${API_URL}/projects/${projectId}`, {
      method: "PATCH",
      body: formData
    })

    await updateProject();
  }

  useEffect(() => {
    updateProject();

    authenticatedFetch(
      `${API_URL}/projects/${projectId}/assignment?lang=${i18next.resolvedLanguage}`
    ).then((response) => {
      if (response.ok) {
        response.text().then((data) => setAssignmentRawText(data));
      }
    });

    fetchMe().then((data) => {
      setMe(data);
    });

  }, [projectId]);

  if (!projectId) return null;

  return (
    <Container>
      <Grid
        container
        direction="row"
        spacing={2}
        margin="2rem 0"
      >
        <Grid item sm={8}>
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
                        <Button variant="outlined" type="link" href={`/${i18next.resolvedLanguage}/courses/${courseData.course_id}`}>
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
          <Box marginTop="2rem">
            <SubmissionCard
              regexRequirements={projectData ? projectData.regex_expressions : []}
              submissionUrl={`${API_URL}/submissions`}
              projectId={projectId}
            />
          </Box>
          {me && me.role == "TEACHER" && (
            <Box
              width="100%">
              <Box display="flex"
                flexDirection="row"
                sx={{
                  justifyContent: "space-around"
                }}
                pt={2}
                width="100%"
              >
                <Box
                  display="flex"
                  flexDirection="row"
                  pt={2}
                  width="100%"
                >
                  <Button
                    type="link"
                    variant="contained"
                    href={location.pathname + "/overview"}
                    sx={{marginRight: 1}}
                  >
                    {t("projectOverview")}
                  </Button>
                  <Button
                    variant="contained"
                    onClick={archiveProject}
                  >
                    {t("archive")}
                  </Button>
                </Box>
                <Box
                  display="flex"
                  flexDirection="row-reverse"
                  pt={2}
                  width="100%">
                  <Button variant="contained" color="error" onClick={() => setAlertVisibility(true)}>
                    Delete
                  </Button>
                </Box>
              </Box>
              <Box display="flex"  style={{width: "100%" }}>
                <div style={{flexGrow: 1}} />
                <Fade
                  style={{width: "fit-content"}}
                  in={alertVisibility}
                  timeout={{ enter: 1000, exit: 1000 }}
                  addEndListener={() => {
                    setTimeout(() => {
                      setAlertVisibility(false);
                    }, 4000);
                  }}
                >
                  <Box sx={{ border: 1, p: 1, bgcolor: 'background.paper' }}>
                    <Typography>Are you sure you want to delete this project</Typography>
                    <Box display="flex"
                      flexDirection="row"
                      sx={{
                        justifyContent: "center"
                      }}
                      pt={2}
                      width="100%"
                    >
                      <Button variant="contained" onClick={deleteProject}>
                        Yes I'm Sure
                      </Button>
                    </Box>
                  </Box>
                </Fade>
              </Box>
              
            </Box>
          )}
        </Grid>
        <Grid item sm={4}>
          <Box marginTop="2rem">
            <DeadlineGrid deadlines={deadlines} minWidth={0} />
          </Box>
        </Grid>
      </Grid>
    </Container>
  );

}
