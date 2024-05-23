import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Container,
  Fade,
  Grid,
  IconButton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import Markdown from "react-markdown";
import {
  useLoaderData,
  useLocation,
  useNavigate,
  useParams,
} from "react-router-dom";
import SubmissionCard from "./SubmissionCard";
import { Course } from "../../../types/course";
import { Title } from "../../../components/Header/Title";
import { authenticatedFetch } from "../../../utils/authenticated-fetch";
import i18next from "i18next";
import { useTranslation } from "react-i18next";
import { Me } from "../../../types/me.ts";
import DeadlineGrid from "../../../components/DeadlineView/DeadlineGrid.tsx";
import { Deadline } from "../../../types/deadline.ts";
import EditIcon from "@mui/icons-material/Edit";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";

const API_URL = import.meta.env.VITE_APP_API_HOST;

interface Project {
  title: string;
  description: string;
  regex_expressions: string[];
  archived: string;
  deadlines: Deadline[];
}

/**
 *
 * @returns - ProjectView component which displays the project details
 * and submissions of the current user for that project
 */
export default function ProjectView() {
  const location = useLocation();

  const { projectData, courseData, assignmentText, isAdmin } =
    useLoaderData() as {
      me: Me;
      projectData: Project;
      courseData: Course;
      assignmentText: string;
      isAdmin: boolean;
    };

  const deadlines = projectData["deadlines"];

  const { t } = useTranslation("translation", { keyPrefix: "projectView" });

  const { projectId } = useParams<{ projectId: string }>();
  const [alertVisibility, setAlertVisibility] = useState(false);
  const [edit, setEdit] = useState(false);
  const [title, setTitle] = useState(projectData["title"]);
  const [description, setDescription] = useState(projectData["description"]);

  const navigate = useNavigate();
  const deleteProject = () => {
    authenticatedFetch(`${API_URL}/projects/${projectId}`, {
      method: "DELETE",
    });
    navigate("/projects");
  };

  const patchTitleAndDescription = async () => {
    setEdit(false);
    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);

    const response = await authenticatedFetch(
      `${API_URL}/projects/${projectId}`,
      {
        method: "PATCH",
        body: formData,
      }
    );

    // Check if the response is ok (status code 2xx)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  };

  const discardEditTitle = () => {
    const title = projectData?.title;
    setEdit(false);
    if (title) setTitle(title);

    if (projectData?.description) setDescription(projectData?.description);
  };

  const archiveProject = async () => {
    const newArchived = !projectData?.archived;
    const formData = new FormData();
    formData.append("archived", newArchived.toString());

    const response = await authenticatedFetch(
      `${API_URL}/projects/${projectId}`,
      {
        method: "PATCH",
        body: formData,
      }
    );

    if (response.ok) {
      navigate(0);
    }
  };

  if (!projectId) return null;

  return (
    <Container>
      <Grid container direction="row" spacing={2} margin="2rem 0">
        <Grid item sm={8}>
          {projectData && (
            <Card>
              <Title title={projectData.title} />
              <CardHeader
                color="secondary"
                title={
                  <Box
                    display="flex"
                    justifyContent="space-between"
                    alignItems="center"
                  >
                    {!edit && <>{projectData.title}</>}
                    {edit && (
                      <>
                        <TextField
                          id="edit-title"
                          label="title"
                          variant="outlined"
                          size="small"
                          defaultValue={title}
                          onChange={(event) => setTitle(event.target.value)}
                        />
                      </>
                    )}
                    {courseData && (
                      <Button
                        variant="outlined"
                        type="link"
                        href={`/${i18next.resolvedLanguage}/courses/${courseData.course_id}`}
                      >
                        {courseData.name}
                      </Button>
                    )}
                  </Box>
                }
                subheader={
                  <Box
                    position="relative"
                    height="100%"
                    sx={{ marginTop: "10px" }}
                  >
                    <Stack direction="row" spacing={2}>
                      {!edit ? (
                        <>
                          <Typography>{projectData.description}</Typography>
                        </>
                      ) : (
                        edit && (
                          <>
                            <TextField
                              id="edit-description"
                              label="description"
                              variant="outlined"
                              size="small"
                              defaultValue={description}
                              onChange={(event) =>
                                setDescription(event.target.value)
                              }
                            />
                          </>
                        )
                      )}
                      <Typography flex="1" />
                    </Stack>
                  </Box>
                }
              />
              <CardContent>
                <Markdown>{assignmentText}</Markdown>
                <Box display="flex" alignItems="flex-end" justifyContent="end">
                  {isAdmin &&
                    (edit ? (
                      <>
                        <IconButton onClick={patchTitleAndDescription}>
                          <CheckIcon />
                        </IconButton>
                        <IconButton onClick={discardEditTitle}>
                          <CloseIcon />
                        </IconButton>
                      </>
                    ) : (
                      <IconButton onClick={() => setEdit(true)}>
                        <EditIcon />
                      </IconButton>
                    ))}
                </Box>
              </CardContent>
            </Card>
          )}
          <Box marginTop="2rem">
            <SubmissionCard
              regexRequirements={
                projectData ? projectData.regex_expressions : []
              }
              submissionUrl={`${API_URL}/submissions`}
              projectId={projectId}
            />
          </Box>
          {isAdmin && (
            <Box width="100%">
              <Box
                display="flex"
                flexDirection="row"
                sx={{
                  justifyContent: "space-around",
                }}
                pt={2}
                width="100%"
              >
                <Box display="flex" flexDirection="row" pt={2} width="100%">
                  <Button
                    type="link"
                    variant="contained"
                    href={location.pathname + "/overview"}
                    sx={{ marginRight: 1 }}
                  >
                    {t("projectOverview")}
                  </Button>
                  <Button variant="contained" onClick={archiveProject}>
                    {t("archive")}
                  </Button>
                </Box>
                <Box
                  display="flex"
                  flexDirection="row-reverse"
                  pt={2}
                  width="100%"
                >
                  <Button
                    variant="contained"
                    color="error"
                    onClick={() => setAlertVisibility(true)}
                  >
                    {t("delete")}
                  </Button>
                </Box>
              </Box>
              <Box display="flex" style={{ width: "100%" }}>
                <div style={{ flexGrow: 1 }} />
                <Fade
                  style={{ width: "fit-content" }}
                  in={alertVisibility}
                  timeout={{ enter: 1000, exit: 1000 }}
                  addEndListener={() => {
                    setTimeout(() => {
                      setAlertVisibility(false);
                    }, 4000);
                  }}
                >
                  <Box sx={{ border: 1, p: 1, bgcolor: "background.paper" }}>
                    <Typography>
                      {t("deleteProjectWarning")}
                    </Typography>
                    <Box
                      display="flex"
                      flexDirection="row"
                      sx={{
                        justifyContent: "center",
                      }}
                      pt={2}
                      width="100%"
                    >
                      <Button variant="contained" onClick={deleteProject}>
                        {t("imSure")}
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
