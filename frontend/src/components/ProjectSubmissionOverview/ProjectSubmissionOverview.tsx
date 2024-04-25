import {Box, Button, Typography} from "@mui/material";
import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import ProjectSubmissionsOverviewDatagrid from "./ProjectSubmissionOverviewDatagrid.tsx";
import download from 'downloadjs';
import {useTranslation} from "react-i18next";
import { get_csrf_cookie } from "../../utils/csrf.ts";
const apiUrl = import.meta.env.VITE_API_HOST

/**
 *  @returns Overview page for submissions
 */
export default function ProjectSubmissionOverview() {

  const { t } = useTranslation('submissionOverview', { keyPrefix: 'submissionOverview' });

  useEffect(() => {
    fetchProject();
  });

  const fetchProject = async () => {
    const response = await fetch(`${apiUrl}/projects/${projectId}`, {
      credentials: 'include',
      headers: {
        "X-CSRF-TOKEN": get_csrf_cookie()
      },
    })
    const jsonData = await response.json();
    setProjectTitle(jsonData["data"].title);

  }

  const downloadProjectSubmissions = async () => {
    await fetch(`${apiUrl}/projects/${projectId}/submissions-download`, {
      credentials: 'include',
      headers: {
        "X-CSRF-TOKEN": get_csrf_cookie()
      },
    })
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