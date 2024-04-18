import {
  Card,
  CardContent,
  CardHeader,
  Container,
  Grid,
  Link,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import { useParams } from "react-router-dom";
import SubmissionCard from "./SubmissionCard";
import { Course } from "../../../types/course";
import { Title } from "../../../components/Header/Title";

const API_URL = import.meta.env.VITE_API_HOST;

interface Project {
  title: string;
  description: string;
}

/**
 *
 * @returns - ProjectView component which displays the project details
 * and submissions of the current user for that project
 */
export default function ProjectView() {
  const { projectId } = useParams<{ projectId: string }>();
  const [projectData, setProjectData] = useState<Project | null>(null);
  const [courseData, setCourseData] = useState<Course | null>(null);
  const [assignmentRawText, setAssignmentRawText] = useState<string>("");

  useEffect(() => {
    fetch(`${API_URL}/projects/${projectId}`, {
      headers: { Authorization: "teacher" },
    }).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          const projectData = data["data"];
          setProjectData(projectData);
          fetch(`${API_URL}/courses/${projectData.course_id}`, {
            headers: { Authorization: "teacher" },
          }).then((response) => {
            if (response.ok) {
              response.json().then((data) => {
                setCourseData(data["data"]);
              });
            }
          });
        });
      }
    });

    fetch(`${API_URL}/projects/${projectId}/assignment`, {
      headers: { Authorization: "teacher" },
    }).then((response) => {
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
              <Title title={projectData.title}/>
              <CardHeader
                color="secondary"
                title={projectData.title}
                subheader={
                  <>
                    <Stack direction="row" spacing={2}>
                      <Typography>{projectData.description}</Typography>
                      <Typography flex="1" />
                      {courseData && (
                        <Link href={`/courses/${courseData.course_id}`}>
                          <Typography>{courseData.name}</Typography>
                        </Link>
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
            submissionUrl={`${API_URL}/submissions`}
            projectId={projectId}
          />
        </Container>
      </Grid>
    </Grid>
  );
}
