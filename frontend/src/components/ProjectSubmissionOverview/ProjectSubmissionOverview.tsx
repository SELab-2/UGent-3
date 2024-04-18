import {Box, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import ProjectSubmissionsOverviewDatagrid from "./ProjectSubmissionOverviewDatagrid.tsx";

const apiUrl = import.meta.env.VITE_API_HOST
const user = "teacher"

/**
 *  @returns Overview page for submissions
 */
export default function ProjectSubmissionOverview() {

  useEffect(() => {
    fetchProject();
  }, []);

  const fetchProject = async () => {
    const response = await fetch(`${apiUrl}/projects/${projectId}`, {
      headers: {
        "Authorization": user
      },
    })
    const jsonData = await response.json();
    setProjectTitle(jsonData["data"].title);

  }

  const [projectTitle, setProjectTitle] = useState<string>("")
  const { projectId } = useParams<{ projectId: string }>();

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      paddingTop="50px"
    >
      <Typography minWidth="440px" variant="h6" align="left">{projectTitle}</Typography>
      <ProjectSubmissionsOverviewDatagrid />
    </Box>
  )
}