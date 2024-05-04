import {
  Alert,
  Button,
  Card,
  CardContent,
  CardHeader,
  Grid,
  IconButton,
  LinearProgress,
  Typography,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { useEffect, useState } from "react";
import FolderDragDrop from "../../../components/FolderUpload/FolderUpload";
import axios from "axios";
import { useTranslation } from "react-i18next";
import SubmissionsGrid from "./SubmissionsGrid";
import { Submission } from "../../../types/submission";

interface SubmissionCardProps {
  regexRequirements?: string[];
  submissionUrl: string;
  projectId: string;
}

/**
 * 
 * @param params - regexRequirements, submissionUrl, projectId
 * @returns - SubmissionCard component which allows the user to submit files
 * and view previous submissions
 */
export default function SubmissionCard({
  regexRequirements,
  submissionUrl,
  projectId,
}: SubmissionCardProps) {
  const { t } = useTranslation('translation', { keyPrefix: 'projectView' });
  const [activeTab, setActiveTab] = useState("submit");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [previousSubmissions, setPreviousSubmissions] = useState<Submission[]>([]);
  const handleFileDrop = (file: File) => {
    setSelectedFile(file);
  };

  useEffect(() => {

    fetch(`${submissionUrl}?project_id=${projectId}`, {
      credentials: 'include'
    }).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          setPreviousSubmissions(data["data"]);
        });
      }
    })
  }, [projectId, submissionUrl]);

  const handleSubmit = async () => {
    const form = new FormData();
    if (!selectedFile) {
      setErrorMessage(t("noFileSelected"));
      return;
    }
    form.append("files", selectedFile);
    form.append("project_id", projectId);
    form.append("uid", "teacher");
    try {
      const response = await axios.post(submissionUrl, form, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: "teacher",
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            setUploadProgress(
              Math.round((progressEvent.loaded * 100) / progressEvent.total)
            );
          }
        },
      });

      if (response.status === 201) {
        setSelectedFile(null);
        setPreviousSubmissions((prev) => [...prev, response.data["data"]]);
        setActiveTab("submissions");
      } else {
        setErrorMessage(t("submitNetworkError"));
      }
    } catch (error) {
      setErrorMessage(t("submitNetworkError"));
    }

    setUploadProgress(null);
  };

  return (
    <Card>
      <CardHeader
        title={
          <>
            <Button onClick={() => setActiveTab("submit")}>{t("submit")}</Button>
            <Button onClick={() => setActiveTab("submissions")}>
              {t("previousSubmissions")}
            </Button>
          </>
        }
      />
      <CardContent>
        {activeTab === "submit" ? (
          <Grid container direction="column" rowGap={1}>
            <Grid item>
              <FolderDragDrop
                regexRequirements={regexRequirements}
                onFileDrop={handleFileDrop}
                onWrongInput={(message) => setErrorMessage(message)}
              />
            </Grid>
            <Grid item>
              {selectedFile && (
                <Typography variant="subtitle1">{`${t("selected")}: ${selectedFile.name}`}</Typography>
              )}
            </Grid>
            <Grid item>
              <IconButton disabled={!selectedFile} onClick={handleSubmit}>
                <SendIcon />
              </IconButton>
            </Grid>
            <Grid item>
              {uploadProgress && (
                <LinearProgress variant="determinate" value={uploadProgress} />
              )}
            </Grid>
            <Grid item>
              {errorMessage && (
                <Alert severity="error" onClose={() => setErrorMessage(null)}>
                  {errorMessage}
                </Alert>
              )}
            </Grid>
          </Grid>
        ) : (
          <SubmissionsGrid submissionUrl={submissionUrl} rows={previousSubmissions}/>
        )}
      </CardContent>
    </Card>
  );
}
