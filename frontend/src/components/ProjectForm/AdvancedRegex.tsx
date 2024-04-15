import {Button, IconButton, Stack, TextField, Tooltip, Typography} from "@mui/material";
import {useTranslation} from "react-i18next";
import React, {useState} from "react";
import {Link} from "react-router-dom";
import {InfoOutlined} from "@mui/icons-material";

interface Props {
  handleSubmit: (regex: string) => void;
  regexError: boolean;
}

/**
 * @returns Component for adding advanced regexes
 */
export default function AdvancedRegex({ handleSubmit, regexError } : Props) {

  const [regex, setRegex] = useState("");
  
  const {t} = useTranslation('projectformTranslation', {keyPrefix: 'advancedRegex'});

  return (
    <Stack
      spacing={2}
    >
      <Typography variant="h6">{t("title")}</Typography>
      <Stack direction="row" style={{display: "flex", alignItems:"center", width: "100%"}}>
        <TextField
          required
          id="outlined-title"
          label="Regex"
          placeholder="Regex"
          error={regexError}
          helperText={regexError ? t("helperRegexText") : ''}
          onChange={event => setRegex(event.target.value)}
        ></TextField>
        <Tooltip title={<Typography>{t("regexInfo")} <Link to="https://cheatography.com/davechild/cheat-sheets/regular-expressions/">{t("cheatsheet")}</Link></Typography>}>
          <IconButton>
            <InfoOutlined/>
          </IconButton>
        </Tooltip>
      </Stack>
      <Button variant="contained" onClick={() => handleSubmit(regex)}>Add custom regex</Button>
    </Stack>
  )
}