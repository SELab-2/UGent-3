import {
  Button,
  Checkbox,
  FormControlLabel,
  FormHelperText,
  Grid,
  InputLabel,
  MenuItem, Select, SelectChangeEvent,
  TextField,
  FormControl, Box, Typography,
  Stack, TableContainer, Table,
  TableRow,
  TableCell,
  TableHead,
  TableBody, Paper,
  Tooltip, IconButton, Tabs, Tab,
} from "@mui/material";
import React, {useEffect, useState} from "react";
import JSZip from 'jszip';
import {useTranslation} from "react-i18next";
import DeleteIcon from "@mui/icons-material/Delete";
import DeadlineCalender from "../Calender/DeadlineCalender.tsx";
import { Deadline } from "../../types/deadline";
import {InfoOutlined} from "@mui/icons-material";
import {Link, useLoaderData, useLocation, useNavigate} from "react-router-dom";
import FolderDragDrop from "../FolderUpload/FolderUpload.tsx";
import TabPanel from "@mui/lab/TabPanel";
import {TabContext} from "@mui/lab";
import FileStuctureForm from "./FileStructureForm.tsx";
import AdvancedRegex from "./AdvancedRegex.tsx";
import RunnerSelecter from "./RunnerSelecter.tsx";
import { authenticatedFetch } from "../../utils/authenticated-fetch.ts";
import i18next from "i18next";

interface Course {
  course_id: string;
  name: string;
  teacher: string;
  ufora_id: string;
}

interface RegexData {
  key: number;
  regex: string;
}

const API_URL = import.meta.env.VITE_APP_API_HOST

/**
 * @returns Form for uploading project
 */
export default function ProjectForm() {

  const { t } = useTranslation('translation', { keyPrefix: 'projectForm' });

  // all the stuff needed for submitting a project
  const [title, setTitle] = useState('');
  const [titleError, setTitleError] = useState(false);

  const [description, setDescription] = useState('');
  const [descriptionError, setDescriptionError] = useState(false);

  const [deadlines, setDeadlines] = useState<Deadline[]>([])
  const [files, setFiles] = useState<string[]>([]);

  const [visibleForStudents, setVisibleForStudents] = useState(false);

  const [regexExpressions, setRegexExpressions] = useState<RegexData[]>([]);
  const [regexError, setRegexError] = useState(false);

  const [assignmentFile, setAssignmentFile] = useState<File>();
  const [filename, setFilename] = useState("");

  const [containsDockerfile, setContainsDockerfile] = useState(false);
  const [containsRuntest, setContainsRuntest] = useState(false);

  const [advanced, setAdvanced] = useState('1');
  const [runner, setRunner] = useState<string>('');
  const [validRunner, setValidRunner] = useState(true);
  const [validSubmission, setValidSubmission] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const courses = useLoaderData() as Course[]

  const [courseId, setCourseId] = useState<string>('');
  const [courseName, setCourseName] = useState<string>('');
  const location = useLocation();

  const navigate = useNavigate();

  useEffect(() =>{
    const urlParams = new URLSearchParams(location.search);
    const initialCourseId = urlParams.get('course_id') || '';
    let initialCourseName = ''
    for( const c of courses){
      const parts = c.course_id.split('/');
      const courseId = parts[parts.length - 1];
      if (courseId === initialCourseId){
        initialCourseName = c.name
      }
    }
    setCourseId(initialCourseId)
    setCourseName(initialCourseName)
  }
  ,[courses,location])

  const handleRunnerSwitch = (newRunner: string) => {
    if (newRunner === t('clearSelected')) {
      setRunner('');
    } else {
      setRunner(newRunner);
    }
  }

  const handleTabSwitch = (_event: React.SyntheticEvent, newAdvanced: string) => {
    setAdvanced(newAdvanced);
  };

  const handleFileUpload2 = async (file: File) => {
    setFiles([]);
    setContainsRuntest(false);
    setContainsDockerfile(false);
    const zip = await JSZip.loadAsync(file);
    const newFiles = [];

    let constainsDocker = false;
    let containsRuntest = false;
    for (const [, zipEntry] of Object.entries(zip.files)) {
      if (!zipEntry.dir) {
        if (zipEntry.name.trim().toLowerCase() === 'dockerfile') {
          constainsDocker = true;
        }
        if (zipEntry.name.trim().toLowerCase() == 'run_tests.sh') {
          containsRuntest = true;
        }
        newFiles.push(zipEntry.name);
      }
    }

    setFiles(newFiles);
    setContainsDockerfile(constainsDocker)
    setContainsRuntest(containsRuntest);
    const {name} = file;
    setAssignmentFile(file)
    setFilename(name);

    if (runner === "CUSTOM") {
      setValidRunner(constainsDocker);
      if (!constainsDocker) {
        setErrorMessage(t("faultySubmission"));
      }
      setValidSubmission(constainsDocker);
    } else if(runner === ''){
      setValidRunner(true);
    }
    else {
      setValidRunner(containsRuntest);
      if(!containsRuntest) {
        setErrorMessage(t("faultySubmission"));
      }
      setValidSubmission(containsRuntest);
    }
  }

  const appendRegex = (r: string) => {
    if (r == '' || regexExpressions.some(reg => reg.regex == r)) {
      setRegexError(true);
      return false;
    }
    setRegexError(false);
    let index;
    const lastRegex = regexExpressions[regexExpressions.length-1];
    if (regexExpressions.length == 0) {
      index = 0;
    } else {
      index = lastRegex.key+1;
    }

    const newRegexExpressions = [...regexExpressions, { key: index, regex: r}];
    setRegexExpressions(newRegexExpressions);

    return true;
  };

  const handleSubmit = async (event: React.MouseEvent<HTMLButtonElement, globalThis.MouseEvent>) => {
    event.preventDefault();

    description == '' ? setDescriptionError(true) : setDescriptionError(false);
    title == '' ? setTitleError(true) : setTitleError(false);

    if (!assignmentFile || !validRunner) {
      setValidSubmission(false);
      setErrorMessage(t("faultySubmission"));
      return;
    }

    const assignmentFileBlob = new Blob([assignmentFile], { type: assignmentFile.type });

    const formData = new FormData();

    // Append fields to the FormData object
    formData.append('title', title);
    formData.append('description', description);
    formData.append('visible_for_students', visibleForStudents.toString());
    formData.append('archived', 'false');
    formData.append('assignment_file', assignmentFileBlob, filename);
    formData.append('course_id', courseId.toString());
    regexExpressions.forEach((expression,) => {
      formData.append(`regex_expressions`, expression.regex);
    });
    deadlines.forEach((deadline: Deadline) => {
      formData.append("deadlines",
        JSON.stringify({
          "deadline": deadline.deadline,
          "description": deadline.description
        })
      );
    });
    if (runner !== '') {
      formData.append("runner", runner);
    }

    const response = await authenticatedFetch(`${API_URL}/projects`, {
      method: "post",
      body: formData,
    })

    if (!response.ok) {
      setValidSubmission(false);
      if (response.status === 403) {
        setErrorMessage(t("unauthorized"));
      }
      else {
        setErrorMessage(t("submissionError"));
      }
      return;
    }

    response.json().then((data) => {
      const projectData = data.data;
      navigate(`/${i18next.language}/projects/${projectData.project_id}`);
    })
  }

  const handleCourseChange = (e: SelectChangeEvent<string>) => {
    const selectedCourseName = e.target.value as string;
    const selectedCourse = courses.find(course => course.name === selectedCourseName);
    if (selectedCourse) {
      setCourseName(selectedCourse.name);
      const parts = selectedCourse.course_id.split('/');
      const courseId = parts[parts.length - 1];
      setCourseId(courseId);
    }
  };

  const handleDeadlineChange = (deadlines: Deadline[]) => {
    setDeadlines(deadlines);
  }

  const removeRegex = (regexToDelete: RegexData) => () => {
    setRegexExpressions((regexes) => regexes.filter((regex) => regex.key !== regexToDelete.key));
  };

  return (
    <Box
      paddingLeft='75p'
      paddingBottom='150px'
    >
      <FormControl
      >
        <Grid
          container
          direction="column"
          spacing={3}
          display='flex'
          alignItems='left'
        >
          <Grid item sx={{ mt: 8 }}>
            <TextField
              sx={{ minWidth: 650 }}
              required
              id="outlined-title"
              label={t("projectTitle")}
              placeholder={t("projectTitle")}
              error={titleError}
              onChange={event => setTitle(event.target.value)}
            />
          </Grid>
          <Grid item>
            <TextField
              sx={{ minWidth: 650 }}
              required
              id="outlined-title"
              label={t("projectDescription")}
              placeholder={t("projectDescription")}
              multiline
              rows={4}
              error={descriptionError}
              onChange={event => setDescription(event.target.value)}
            />
          </Grid>
          <Grid item>
            <FormControl>
              <InputLabel id="course-simple-select-label">{t("projectCourse")}</InputLabel>
              <Select
                labelId="course-simple-select-label"
                id="course-simple-select"
                value={courseName}
                label={t("projectCourse")}
                onChange={handleCourseChange}
              >
                {courses.map(course => (
                  <MenuItem key={course.course_id} value={course.name}>
                    {course.name}
                  </MenuItem>
                ))}
              </Select>
              <FormHelperText>{t("selectCourseText")}</FormHelperText>
            </FormControl>
          </Grid>
          <Grid item>
            <DeadlineCalender
              deadlines={[]}
              onChange={(deadlines: Deadline[]) => handleDeadlineChange(deadlines)}
              editable={true} />
            <TableContainer component={Paper}>
              <Table sx={{ minWidth: 650 }}>
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
          </Grid>
          <Grid item>
            <Stack direction="row" style={{display: "flex", alignItems:"center"}}>
              <FormControlLabel control={<Checkbox defaultChecked />} label={t("visibleForStudents")} onChange={e=>setVisibleForStudents((e.target as HTMLInputElement).checked)}/>
              <Tooltip title={<Typography variant="h6">{t("visibleForStudentsTooltip")}</Typography>}>
                <IconButton>
                  <InfoOutlined/>
                </IconButton>
              </Tooltip>
            </Stack>
          </Grid>
          <Grid item>
          </Grid>
          <Grid item>
            <Stack direction="row" style={{display: "flex", alignItems:"center", paddingBottom: "40px"}}>
              <FolderDragDrop onFileDrop={file => handleFileUpload2(file)} regexRequirements={[]} />
              <Tooltip style={{ height: "40%" }} title={<Typography variant="h6">{t("fileInfo")}: <Link to="/">{t("userDocs")}</Link></Typography>}>
                <IconButton>
                  <InfoOutlined/>
                </IconButton>
              </Tooltip>
            </Stack>
            <TableContainer component={Paper}>
              <Table sx={{ minWidth: "350px" }}>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: 'bold' }}>{t("zipFile")}: {filename}</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {files.length === 0 ? ( // Check if files is empty
                    <TableRow>
                      <TableCell colSpan={1} align="center">{t("noFilesPlaceholder")}</TableCell> {/* Placeholder row */}
                    </TableRow>
                  ) : (
                    files.map((file, index) => (
                      <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                        <TableCell component="th" scope="row">{file}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
            {filename !== "" && (!containsRuntest && !containsDockerfile) && (
              <Typography style={{color: 'orange', paddingTop: "20px" }}>
                {t("testWarning")} ⚠️
              </Typography>
            )}
          </Grid>
          <Grid item sx={{ minWidth: "722px" }}>
            <TabContext value={advanced}>
              <Tabs value={advanced} onChange={handleTabSwitch}>
                <Tab label="File restrictions" value="1"/>
                <Tab label="Advanced mode" value="0"/>
              </Tabs>
              <TabPanel value="1"><FileStuctureForm handleSubmit={appendRegex} regexError={regexError}/></TabPanel>
              <TabPanel value="0"><AdvancedRegex handleSubmit={appendRegex} regexError={regexError} /></TabPanel>
            </TabContext>
          </Grid>
          <Grid item>
            <TableContainer component={Paper}>
              <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: 'bold' }}>Regex</TableCell>
                    <TableCell></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {regexExpressions.length === 0 ? ( // Check if regexExpressions is empty
                    <TableRow>
                      <TableCell colSpan={2} align="center">{t("noRegexPlaceholder")}</TableCell> {/* Placeholder row */}
                    </TableRow>
                  ) : (
                    regexExpressions.map((regexData: RegexData) => (
                      <TableRow key={regexData.key}>
                        <TableCell>{regexData.regex}</TableCell>
                        <TableCell align="right">
                          <IconButton onClick={removeRegex(regexData)}>
                            <DeleteIcon/>
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
          <Grid item>
            <RunnerSelecter handleSubmit={handleRunnerSwitch} runner={runner} containsDocker={containsDockerfile} containsRuntests={containsRuntest} isValid={validRunner} setIsValid={setValidRunner} />
          </Grid>
          <Grid item>
            <Button variant="contained" onClick={e => {
              return handleSubmit(e);
            }
            }>{t("uploadProject")}</Button>
            {
              !validSubmission && (
                <Typography style={{color: 'red', paddingTop: "20px" }}>
                  {errorMessage} ⚠️
                </Typography>
              )
            }
          </Grid>
        </Grid>
      </FormControl>
    </Box>
  )
}