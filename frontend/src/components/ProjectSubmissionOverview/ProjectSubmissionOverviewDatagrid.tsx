import {DataGrid, GridColDef, GridRenderCellParams} from "@mui/x-data-grid";
import { Box, IconButton } from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { green, red } from "@mui/material/colors";
import CancelIcon from "@mui/icons-material/Cancel";
import DownloadIcon from "@mui/icons-material/Download";
import download from "downloadjs";
import { authenticatedFetch } from "../../utils/authenticated-fetch";
import { Submission } from "../../types/submission";

const APIURL = import.meta.env.VITE_APP_API_HOST;

/**
 * @returns unique id for datarows
 */
function getRowId(row: Submission) {
  return row.submission_id;
}

const fetchSubmissionsFromUser = async (submission_id: string) => {
  await authenticatedFetch(`${APIURL}/submissions/${submission_id}/download`)
    .then((res) => {
      return res.blob();
    })
    .then((blob) => {
      download(blob, `submissions_${submission_id}.zip`);
    });
};

const editGrade = (submission: Submission, oldSubmission: Submission) => {
  const submission_id = submission.submission_id;
  const newGrade = submission.grading;

  if (newGrade < 0 || newGrade > 20) {
    return oldSubmission;
  }

  const formData = new FormData();
  formData.append('grading', newGrade.toString());

  authenticatedFetch(`${APIURL}/submissions/${submission_id}`, {
    method: "PATCH",
    body: formData
  })

  return submission
};

const columns: GridColDef<Submission>[] = [
  { field: "submission_id", headerName: "Submission ID", flex: 0.4, editable: false },
  { field: "display_name", headerName: "Student", width: 160, flex: 0.4, editable: false },
  {
    field: "grading",
    headerName: "Grading",
    editable: true,
    flex: 0.2,
  },
  {
    field: "submission_status",
    headerName: "Status",
    editable: false,
    renderCell: (params: GridRenderCellParams<Submission>) => (
      <>
        {params.row.submission_status === "SUCCESS" ? (
          <CheckCircleIcon sx={{ color: green[500] }} />
        ) : (
          <CancelIcon sx={{ color: red[500] }} />
        )}
      </>
    ),
  },
  {
    field: "submission_path",
    headerName: "Download",
    renderCell: (params: GridRenderCellParams<Submission>) => (
      <IconButton
        onClick={() => fetchSubmissionsFromUser(params.row.submission_id)}
      >
        <DownloadIcon />
      </IconButton>
    ),
  },
];

/**
 * @returns the datagrid for displaying submissions
 */
export default function ProjectSubmissionsOverviewDatagrid({
  submissions,
}: {
  submissions: Submission[];
}) {
  return (
    <Box my={4}>
      <DataGrid
        getRowId={getRowId}
        rows={submissions}
        columns={columns}
        pageSizeOptions={[20]}
        disableRowSelectionOnClick
        processRowUpdate={(updatedRow, oldRow) =>
          editGrade(updatedRow, oldRow)
        }
      />
    </Box>
  );
}
