import {
  Container,
  Grid,
  Link,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import { useParams } from "react-router-dom";
import { Project } from "../../types/project.ts";

const API_URL = import.meta.env.VITE_API_HOST;

export default function Home(): React.JSX.Element {
  const [projects, setProjects] = useState<Project[] | []>([]);

  useEffect(() => {
    fetch(`${API_URL}/projects/`, {
      headers: { Authorization: "teacher" }
    }).then((respone) => {
      if (respone.ok) {
        respone.json().then((projectsData) => {
          projectsData.forEach((project: any) => {
            fetch(`${API_URL}/courses/${project.projectId}`, {
              headers: { Authorization: "teacher" },
            }).then((response) => {
              response.json().then((project) => {
                setProjects([...projects, project["data"]]);
              });
              fetch(`${API_URL}/courses/${project["data"].course_id}`, {
                headers: { Authorization: "teacher" }
              }).then((response) => {
                response.json().then((course) => {
                  projects[-1].course_title = course["data"].title;
                })
              })
            });
          })
        })
      }
    })
  });

  return (
    <Grid
      width="100%"
      container
      rowGap="2rem"
      margin="2rem 0"
    >
      <Grid item>
        <Stack>
          { projects[0].title }
        </Stack>
      </Grid>
    </Grid>
  )
}