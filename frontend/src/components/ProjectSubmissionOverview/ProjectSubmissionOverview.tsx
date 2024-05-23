import { Box, Button, Typography } from "@mui/material";
import { useLoaderData, useParams } from "react-router-dom";
import ProjectSubmissionsOverviewDatagrid from "./ProjectSubmissionOverviewDatagrid.tsx";
import download from "downloadjs";
import { useTranslation } from "react-i18next";
import { authenticatedFetch } from "../../utils/authenticated-fetch.ts";
import { Project } from "../Courses/CourseUtils.tsx";
import { Submission } from "../../types/submission.ts";

const APIURL = import.meta.env.VITE_APP_API_HOST;

/**
 *  @returns Overview page for submissions
 */
export default function ProjectSubmissionOverview() {
  const { t } = useTranslation("submissionOverview", {
    keyPrefix: "submissionOverview",
  });

  const { projectId } = useParams<{ projectId: string }>();
  const { projectData, submissionsWithUsers } = useLoaderData() as {
    projectData: Project;
    submissionsWithUsers: Submission[];
  };

  const downloadProjectSubmissions = async () => {
    await authenticatedFetch(
      `${APIURL}/projects/${projectId}/submissions-download`
    )
      .then((res) => {
        return res.blob();
      })
      .then((blob) => {
        download(blob, "submissions.zip");
      });
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      paddingTop="50px"
    >
      <Box width="40%">
        <Typography minWidth="440px" variant="h6" align="left">
          {projectData["title"]}
        </Typography>
        <ProjectSubmissionsOverviewDatagrid
          submissions={submissionsWithUsers}
        />
      </Box>
      <Button onClick={downloadProjectSubmissions} variant="contained">
        {t("downloadButton")}
      </Button>
    </Box>
  );
}
