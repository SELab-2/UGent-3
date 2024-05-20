import {Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";
import {Deadline} from "../../types/deadline.ts";
import {useTranslation} from "react-i18next";

interface Props {
  deadlines: Deadline[];
  minWidth: number
}

/**
 *
 */
export default function DeadlineGrid({deadlines, minWidth}: Props) {

  const { t } = useTranslation('translation', { keyPrefix: 'projectForm' });

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: minWidth }}>
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: 'bold' }}>{t("deadline")}</TableCell>
            <TableCell sx={{ fontWeight: 'bold' }} align="right">{t("description")}</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {deadlines.length === 0 ? ( // Check if deadlines is empty
            <TableRow>
              <TableCell colSpan={2} align="center">{t("noDeadlinesPlaceholder")}</TableCell>
            </TableRow>
          ) : (
            deadlines.map((deadline, index) => (
              <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                <TableCell component="th" scope="row">{deadline.deadline}</TableCell>
                <TableCell align="right">{deadline.description}</TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  )
}