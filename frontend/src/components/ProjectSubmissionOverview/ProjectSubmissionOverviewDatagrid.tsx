import {
  DataGrid,
  GridEditInputCell,
  GridPreProcessEditCellProps,
  GridRenderCellParams,
  GridRenderEditCellParams
} from "@mui/x-data-grid";
import {Box, IconButton, styled, Tooltip, tooltipClasses, TooltipProps} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { green, red } from "@mui/material/colors";
import CancelIcon from "@mui/icons-material/Cancel";
import DownloadIcon from "@mui/icons-material/Download";
import download from "downloadjs";
import { authenticatedFetch } from "../../utils/authenticated-fetch";
import { Submission } from "../../types/submission";
import {useTranslation} from "react-i18next";
import {TFunction} from "i18next";
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

const editGrade = (submission: Submission, errorMessage: string) => {
  const submission_id = submission.submission_id;
  const newGrade = submission.grading;

  if (newGrade < 0 || newGrade > 20) {
    throw new Error(errorMessage);
  }

  const formData = new FormData();
  formData.append('grading', newGrade.toString());

  authenticatedFetch(`${APIURL}/submissions/${submission_id}`, {
    method: "PATCH",
    body: formData
  })

  return submission
};

const StyledTooltip = styled(({ className, ...props }: TooltipProps) => (
  <Tooltip {...props} classes={{ popper: className }} />
))(({ theme }) => ({
  [`& .${tooltipClasses.tooltip}`]: {
    backgroundColor: theme.palette.error.main,
    color: theme.palette.error.contrastText,
  },
}));

/**
 * @returns Component for input edit cell
 */
function NameEditInputCell(props: GridRenderEditCellParams) {
  const { error, msg } = props;

  return (
    <StyledTooltip open={!!error} title={msg}>
      <GridEditInputCell {...props} />
    </StyledTooltip>
  );
}

/**
 * @returns component for passing params
 */
function renderEditScore(params: GridRenderEditCellParams) {
  return <NameEditInputCell {...params} />;
}

const getTranslatedRows = (t: TFunction<string, string>) => {
  return [
    { field: "submission_id", headerName: t("submissionID"), flex: 0.4, editable: false },
    { field: "display_name", headerName: t("student"), width: 160, flex: 0.4, editable: false },
    {
      field: "grading",
      headerName: t("grading"),
      editable: true,
      flex: 0.2,
      preProcessEditCellProps: (params: GridPreProcessEditCellProps) => {
        const hasError = params.props.value > 20 || params.props.value < 0;
        return { ...params.props, error: hasError, msg: t("scoreError") };
      },
      renderEditCell: renderEditScore
    },
    {
      field: "submission_status",
      headerName: t("status"),
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
      headerName: t("download"),
      renderCell: (params: GridRenderCellParams<Submission>) => (
        <IconButton
          onClick={() => fetchSubmissionsFromUser(params.row.submission_id)}
        >
          <DownloadIcon />
        </IconButton>
      ),
    },
  ];
}

/**
 * @returns the datagrid for displaying submissions
 */
export default function ProjectSubmissionsOverviewDatagrid({
  submissions,
}: {
  submissions: Submission[];
}) {

  const { t } = useTranslation('submissionOverview', { keyPrefix: 'submissionOverview' });

  const errorMsg = t("scoreError");

  return (
    <Box my={4}>
      <DataGrid
        getRowId={getRowId}
        rows={submissions}
        columns={getTranslatedRows(t)}
        pageSizeOptions={[20]}
        disableRowSelectionOnClick
        processRowUpdate={(updatedRow) =>
          editGrade(updatedRow, errorMsg)
        }
      />
    </Box>
  );
}
