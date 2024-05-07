import {Box, Button, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import ProjectSubmissionsOverviewDatagrid from "./ProjectSubmissionOverviewDatagrid.tsx";
import download from 'downloadjs';
import {useTranslation} from "react-i18next";
import { authenticatedFetch } from "../../utils/authenticated-fetch.ts";
const apiUrl = import.meta.env.VITE_APP_API_HOST;

/**
 *  @returns Overview page for submissions
 */
export default function ProjectSubmissionOverview() {

  const { t } = useTranslation('submissionOverview', { keyPrefix: 'submissionOverview' });

  useEffect(() => {
    fetchProject();
  });

  const fetchProject = async () => {
    const response = await authenticatedFetch(`${apiUrl}/projects/${projectId}`)
    const jsonData = await response.json();
    setProjectTitle(jsonData["data"].title);

  }

  const downloadProjectSubmissions = async () => {
    await authenticatedFetch(`${apiUrl}/projects/${projectId}/submissions-download`)
      .then(res => {
        return res.blob();
      })
      .then(blob => {
        download(blob, 'submissions.zip');
      });
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
      <Box width="40%">
        <Typography minWidth="440px" variant="h6" align="left">{projectTitle}</Typography>
        <ProjectSubmissionsOverviewDatagrid />
      </Box>
      <Button onClick={downloadProjectSubmissions} variant="contained">{t("downloadButton")}</Button>
    </Box>
  )
}