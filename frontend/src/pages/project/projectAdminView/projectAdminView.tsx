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
import { authenticatedFetch } from "../../../utils/authenticated-fetch";
import i18next from "i18next";
import {useTranslation} from "react-i18next";
import {Deadline} from "../../../types/deadline.ts";
import ProjectAdminViewDeadlineDatagrid from "./projectAdminViewDeadlineDatagrid.tsx";

const API_URL = import.meta.env.VITE_APP_API_HOST;

interface Project {
  title: string;
  description: string;
  regex_expressions: string[];
}

/**
 *
 * @returns - ProjectAdminView component which displays the project details
 * and submissions of the current admin for that project
 */
export default function ProjectAdminView() {

  const { t } = useTranslation('projectAdminView', { keyPrefix: 'projectsAdminView' });

  const { projectId } = useParams<{ projectId: string }>();
  const [projectData, setProjectData] = useState<Project | null>(null);
  const [deadlines, setDeadlines] = useState<Deadline[]>([])

  useEffect(() => {
    authenticatedFetch(`${API_URL}/projects/${projectId}`).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          const project = data["data"]
          setProjectData(project);
          setDeadlines(project.deadlines)
        })
      }
    })
  }, []);

  return (
    <Grid
      width="100%"
      container
      direction="column"
      rowGap="2rem"
      margin="2rem 0"
    >
      <Grid item>
        {
          projectData && (
            <Card>
              <Title title={projectData.title} />
              <CardHeader
                color="secondary"
                title={t("projectInfo")}
              ></CardHeader>
              <CardContent>
                <Typography variant="h6">{projectData.title}</Typography>
                <Typography>{projectData.description}</Typography>
              </CardContent>
              <CardContent>
                <Typography></Typography>
              </CardContent>
              <CardContent>
                <ProjectAdminViewDeadlineDatagrid deadlines={deadlines}></ProjectAdminViewDeadlineDatagrid>
              </CardContent>
            </Card>
          )
        }
      </Grid>
    </Grid>
  );
}
