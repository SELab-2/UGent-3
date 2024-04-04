import {
  Card,
  CardHeader,
  Container,
  Grid,
  Link,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const API_URL = import.meta.env.VITE_API_HOST;

interface Project {
  title: string;
  description: string;
}

export default function ProjectView() {
  const { projectId } = useParams<{ projectId: string }>();
  const [projectData, setProjectData] = useState<Project | null>(null);
  const [courseData, setCourseData] = useState<any | null>(null);

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
                console.log(data);
                setCourseData(data["data"]);
              });
            }
          });
        });
      }
    });
  }, [projectId]);

  return (
    <Grid
      width="100%"
      container
      direction="column"
      rowGap="2rem"
      marginTop="2rem"
    >
      <Grid item sm={12}>
        <Container>
          {projectData && (
            <Card>
              <CardHeader
                title={projectData.title}
                subheader={
                  <>
                    <Stack direction="row" spacing={2}>
                      <Typography>{projectData.description}</Typography>
                      <Typography flex="1" />
                      {courseData && (
                        <Link href={`/courses/${courseData.course_id}`} >
                          <Typography>{courseData.name}</Typography>
                        </Link>
                      )}
                    </Stack>
                  </>
                }
              />
            </Card>
          )}
        </Container>
      </Grid>
      <Grid item sm={12}>
        <Container>
          <Card>
            <CardHeader title="Tasks" />
          </Card>
        </Container>
      </Grid>
    </Grid>
  );
}
