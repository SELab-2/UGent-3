import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
  Typography,
  Tooltip,
  Stack, IconButton
} from "@mui/material";
import { Dispatch, SetStateAction } from "react";
import { useTranslation } from "react-i18next";
import {InfoOutlined} from "@mui/icons-material";
import {Link} from "react-router-dom";

interface Props {
  handleSubmit: (runner: string) => void;
  runner: string;
  containsDocker: boolean;
  containsRuntests: boolean;
  isValid: boolean;
  setIsValid: Dispatch<SetStateAction<boolean>>;
}

/**
 * @returns Component for selecting an appropriate runner
 */
export default function RunnerSelecter({ handleSubmit, runner, containsDocker, containsRuntests, isValid, setIsValid }: Props) {

  const { t } = useTranslation('projectformTranslation', { keyPrefix: 'runnerComponent' });

  const runnerMapping: { [key: string]: boolean } = {
    "GENERAL": containsRuntests,
    "PYTHON": containsRuntests,
    "CUSTOM": containsDocker,
    [t("clearSelected")]: true
  }

  const handleRunnerChange = (event: SelectChangeEvent) => {
    const runner: string = event.target.value as string;
    handleSubmit(runner);
    setIsValid(runnerMapping[runner]);
  }

  return (
    <>
      <Stack direction="row">
        <FormControl sx={{ minWidth: "110px" }}>
          <InputLabel id="select-runner-label">Runner</InputLabel>
          <Select
            labelId="select-runner-label"
            id="runner-select"
            value={runner}
            label="Runner"
            onChange={handleRunnerChange}
            sx={{maxWidth: '260px'}}
          >
            <MenuItem disabled value="" key={0}>
                Select a runner
            </MenuItem>
            {Object.keys(runnerMapping).map((runnerOption, index) => (
              runnerOption !== t("clearSelected") && <MenuItem key={index + 1} value={runnerOption}>
                <Typography>{runnerOption}</Typography>
              </MenuItem>
            ))}
            <MenuItem value={t("clearSelected")}>{t("clearSelected")}</MenuItem>
          </Select>
        </FormControl>
        <Tooltip title={<Typography variant="h6">{t("tooltipRunner")}: <Link to="/">{t("userDocs")}</Link></Typography>}>
          <IconButton>
            <InfoOutlined/>
          </IconButton>
        </Tooltip>
      </Stack>
      {
        !isValid && (
          <Typography style={{ color: 'red', paddingTop: "20px" }}>
            {t("testWarning")} ⚠️
          </Typography>
        )
      }
    </>
  )
}
