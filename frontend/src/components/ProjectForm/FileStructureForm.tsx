import {Autocomplete, Button, Stack, TextField, Typography} from "@mui/material";
import {useState} from "react";
import {useTranslation} from "react-i18next";

interface Props {
  handleSubmit: (regex: string) => boolean;
  regexError: boolean;
}

/**
 * @returns Component for adding file restrictions
 */
export default function FileStuctureForm({ handleSubmit, regexError } : Props) {

  const extensions = [".txt", ".pdf", ".zip", ".7z", ".csv", ".doc", ".py", ".java", ".c"];

  const {t} = useTranslation('projectformTranslation', {keyPrefix: 'filestructure'});

  const [startsWith, setStartsWith] = useState("");
  const [endsWith, setEndsWith] = useState("");
  const [contains, setContains] = useState("");
  const [extension, setExtension] = useState("");

  const handleExtensionChange = (value: string | null) => {
    if (value) {
      setExtension(value);
    }
  }

  const handleRegexSubmit = () => {
    let regex = "";
    if (startsWith) {
      regex += "^" + startsWith
    }
    if (contains) {
      regex += "*" + contains + "*";
    } else if (startsWith || endsWith) {
      regex += "*"
    }
    if (endsWith != "" && extension != "") {
      regex += endsWith + extension + "$";
    } else if (endsWith != "") {
      regex += endsWith + "$";
    }
    const result = handleSubmit(regex);
    if (result) {
      setStartsWith("");
      setExtension("");
      setEndsWith("");
      setContains("");
    }
  }

  return (
    <Stack
      spacing={2}
    >
      <Typography variant="h6">{t("title")}</Typography>
      <TextField
        sx={{minWidth: 650}}
        id="startsWith"
        label={t("startsWith")}
        placeholder={t("startsWith")}
        error={regexError}
        value={startsWith}
        onChange={e => setStartsWith(e.target.value)}
      />
      <TextField
        sx={{minWidth: 650}}
        id="endsWith"
        label={t("endsWith")}
        placeholder={t("endsWith")}
        error={regexError}
        value={endsWith}
        onChange={e => setEndsWith(e.target.value)}
      />
      <TextField
        sx={{minWidth: 650}}
        id="contains"
        label={t("contains")}
        placeholder={t("contains")}
        error={regexError}
        value={contains}
        onChange={e => setContains(e.target.value)}
      />
      <Autocomplete
        id="extension"
        freeSolo
        value={extension}
        onChange={(_event, value) => handleExtensionChange(value)}
        renderInput={(params) => <TextField {...params} label={t('fileExtension')} error={regexError} helperText={regexError ? t("helperRegexText") : ''} />}
        options={extensions.map((t) => t)}
      />
      <Button variant="contained" onClick={() => handleRegexSubmit()}>
        {t('addRestriction')}
      </Button>
    </Stack>
  )
}