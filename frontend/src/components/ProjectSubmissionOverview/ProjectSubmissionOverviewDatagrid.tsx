import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {DataGrid, GridColDef, GridRenderCellParams} from "@mui/x-data-grid";
import {Box, IconButton} from "@mui/material";
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { green, red } from '@mui/material/colors';
import CancelIcon from '@mui/icons-material/Cancel';
import DownloadIcon from '@mui/icons-material/Download';
import download from "downloadjs";
import { authenticatedFetch } from "../../utils/authenticated-fetch";

const apiUrl = import.meta.env.VITE_API_HOST

  interface Submission {
    grading: string;
    project_id: string;
    submission_id: string;
    submission_path: string;
    submission_status: string;
    submission_time: string;
    uid: string;
  }

/**
 * @returns unique id for datarows
 */
function getRowId(row: Submission) {
  return row.submission_id;
}

const fetchSubmissionsFromUser = async (submission_id: string) => {
  await authenticatedFetch(`${apiUrl}/submissions/${submission_id}/download`)
    .then(res => {
      return res.blob();
    })
    .then(blob => {
      download(blob, `submissions_${submission_id}.zip`);
    });
}

const columns: GridColDef<Submission>[] = [
  { field: 'submission_id', headerName: 'Submission ID', flex: 0.4 },
  { field: 'uid', headerName: 'Student ID', width: 160, flex: 0.4 },
  {
    field: 'grading',
    headerName: 'Grading',
    editable: true,
    flex: 0.2
  },
  {
    field: 'submission_status',
    headerName: 'Status',
    renderCell: (params: GridRenderCellParams<Submission>) => (
      <>
        {
          params.row.submission_status === "SUCCESS" ? (
            <CheckCircleIcon sx={{ color: green[500] }} />
          ) : <CancelIcon sx={{ color: red[500] }}/>
        }
      </>
    )
  },
  {
    field: 'submission_path',
    headerName: 'Download',
    renderCell: (params: GridRenderCellParams<Submission>) => (
      <IconButton onClick={() => fetchSubmissionsFromUser(params.row.submission_id)}>
        <DownloadIcon />
      </IconButton>
    )
  }];

/**
 * @returns the datagrid for displaying submissiosn
 */
export default function ProjectSubmissionsOverviewDatagrid() {
  const { projectId } = useParams<{ projectId: string }>();
  const [submissions, setSubmissions]  = useState<Submission[]>([])

  useEffect(() => {
    fetchLastSubmissionsByUser();
  });

  const fetchLastSubmissionsByUser = async () => {
    const response = await authenticatedFetch(`${apiUrl}/projects/${projectId}/latest-per-user`)
    const jsonData = await response.json();
    setSubmissions(jsonData.data);
  }

  return (
    <Box
      my={4}
    >
      <DataGrid
        getRowId={getRowId}
        rows={submissions}
        columns={columns}
        pageSizeOptions={[20]}
        disableRowSelectionOnClick
      />
    </Box>
  )
}