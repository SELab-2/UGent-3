import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import {DataGrid, GridColDef, GridRenderCellParams} from "@mui/x-data-grid";
import {Box} from "@mui/material";
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { green, red } from '@mui/material/colors';
import CancelIcon from '@mui/icons-material/Cancel';

const apiUrl = import.meta.env.VITE_API_HOST
const user = "teacher"

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
 *
 */
function getRowId(row: Submission) {
  return row.submission_id;
}

const columns: GridColDef<Submission> = [
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
    renderCell: (params: Submission) => (
        //<>
        //  {console.log(params.row)}
        //  <CheckCircleIcon sx={{ color: green[500] }}/>
        //</>
        <>
        {
          params.row.submission_status === "SUCCESS" ? (
              <CheckCircleIcon sx={{ color: green[500] }} />
          ) : <CancelIcon sx={{ color: red[500] }}/>
        }
        </>
    ),
  }
];

/**
 *
 */
export default function ProjectSubmissionsOverviewDatagrid() {
  const { projectId } = useParams<{ projectId: string }>();
  const [submissions, setSubmissions]  = useState<Submission[]>([])

  useEffect(() => {
    fetchLastSubmissionsByUser();
  }, []);

  const fetchLastSubmissionsByUser = async () => {
    const response = await fetch(`${apiUrl}/projects/${projectId}/latest-per-user`, {
      headers: {
        "Authorization": user
      },
    })
    const jsonData = await response.json();
    setSubmissions(jsonData.data);
  }

  return (
    <Box
      my={4}
      width="60%"
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