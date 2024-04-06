import { DataGrid, GridColDef } from "@mui/x-data-grid";
import DownloadIcon from "@mui/icons-material/Download";
import { IconButton } from "@mui/material";
import { useTranslation } from "react-i18next";
import { timeDifference } from "../../../utils/date-utils";
import { Submission } from "../../../types/submission";

interface SubmissionsGridProps {
  submissionUrl: string;
  rows: Submission[];
}

/**
 * 
 * @param param - submissionUrl, rows
 * @returns - SubmissionsGrid component which displays the submissions of the current user
 */
export default function SubmissionsGrid({
  submissionUrl,
  rows,
}: SubmissionsGridProps) {
  const { t } = useTranslation("translation", {
    keyPrefix: "projectView.submissionGrid",
  });

  const stateMapper = {
    LATE: t("late"),
    FAIL: t("fail"),
    RUNNING: t("running"),
    SUCCESS: t("success"),
  };

  const columns: GridColDef[] = [
    {
      field: "id",
      type: "string",
      width: 50,
      headerName: "",
    },
    {
      field: "submission_time",
      headerName: t("submitTime"),
      type: "string",
      flex: 1,
      valueFormatter: (value) => timeDifference(value),
    },
    {
      field: "submission_status",
      headerName: t("status"),
      type: "string",
      flex: 1,
      valueFormatter: (value) => stateMapper[value],
    },
    {
      field: "actions",
      type: "actions",
      width: 50,
      getActions: (props) => [
        <IconButton href={`${submissionUrl}/${props.id}`}>
          <DownloadIcon />
        </IconButton>,
      ],
    },
  ];

  return (
    <DataGrid
      autosizeOnMount
      columns={columns}
      disableColumnResize
      disableColumnFilter
      disableColumnSelector
      disableColumnSorting
      disableDensitySelector
      disableColumnMenu
      disableVirtualization
      showColumnVerticalBorder={false}
      showCellVerticalBorder={false}
      disableRowSelectionOnClick
      disableEval
      disableMultipleRowSelection
      hideFooter
      autoHeight
      sortModel={[{ field: "submission_time", sort: "desc" }]}
      getRowId={(row) => {
        const urlTags = row.submission_id.split("/");
        return urlTags[urlTags.length - 1];
      }}
      rows={rows}
    />
  );
}
