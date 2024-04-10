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
  Tooltip, IconButton,
} from "@mui/material";
import React, {useEffect, useState} from "react";
import JSZip from 'jszip';
import {useTranslation} from "react-i18next";
import DeleteIcon from "@mui/icons-material/Delete";
import DeadlineCalender from "../Calender/DeadlineCalender.tsx";
import { Deadline } from "../../types/deadline";
import {InfoOutlined} from "@mui/icons-material";
import {Link} from "react-router-dom";
import FolderDragDrop from "../FolderUpload/FolderUpload.tsx";

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

const apiUrl = import.meta.env.VITE_APP_API_URL
const user = "Gunnar"

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

  const [regex, setRegex] = useState<string>("");
  const [regexExpressions, setRegexExpressions] = useState<RegexData[]>([]);
  const [regexError, setRegexError] = useState(false);

  const [assignmentFile, setAssignmentFile] = useState<File>();
  const [filename, setFilename] = useState("");

  const [courses, setCourses] = useState<Course[]>([]);
  const [courseId, setCourseId] = useState<string>('');
  const [courseName, setCourseName] = useState<string>('');

  const [containsTests, setContainsTests] = useState(true);

  useEffect(() => {
    fetchCourses();
  }, [regexError]);

  const handleFileUpload2 = async (file: File) => {
    const zip = await JSZip.loadAsync(file);
    const newFiles = files.slice();

    let containsTestsFlag = false; // Initialize flag
    for (const [, zipEntry] of Object.entries(zip.files)) {
      if (!zipEntry.dir) {
        // Check if the file is a Dockerfile
        if (zipEntry.name.trim().toLowerCase() === 'dockerfile' || zipEntry.name.trim().toLowerCase() == 'run_tests.sh') {
          containsTestsFlag = true;
        }
        newFiles.push(zipEntry.name);
      }
    }

    setFiles(newFiles);
    setContainsTests(containsTestsFlag);
    const {name} = file;
    setAssignmentFile(file)
    setFilename(name);

  }

  const fetchCourses = async () => {
    const response = await fetch(`${apiUrl}/courses?teacher=${user}`, {
      headers: {
        "Authorization": user
      },
    })
    const jsonData = await response.json();
    setCourses(jsonData.data);
  }

  const appendRegex = () => {

    if (regex == '' || regexExpressions.some(reg => reg.regex == regex)) {
      setRegexError(true);
      return;
    }
    setRegexError(false);
    let index;
    const lastRegex = regexExpressions[regexExpressions.length-1];
    if (regexExpressions.length == 0) {
      index = 0;
    } else {
      index = lastRegex.key+1;
    }

    const newRegexExpressions = [...regexExpressions, { key: index, regex: regex}];
    setRegexExpressions(newRegexExpressions);
  };

  const handleSubmit = async (event: React.MouseEvent<HTMLButtonElement, globalThis.MouseEvent>) => {
    event.preventDefault();

    description == '' ? setDescriptionError(true) : setDescriptionError(false);
    title == '' ? setTitleError(true) : setTitleError(false);

    if (!assignmentFile) {
      return;
    }

    const assignmentFileBlob = new Blob([assignmentFile], { type: assignmentFile.type });
    console.log("blob");
    console.log(assignmentFileBlob);

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
    console.log(formData)

    const response = await fetch(`${apiUrl}/projects`, {
      method: "post",
      headers: {
        "Authorization": user
      },
      body: formData
    })

    if (!response.ok) {
      throw new Error(t("uploadError"));
    }
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

  const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Enter') {
      appendRegex();
    }
  };

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
                  {deadlines.map((deadline, index) => (
                    <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                      <TableCell component="th" scope="row">{deadline.deadline}</TableCell>
                      <TableCell align="right">{deadline.description}</TableCell>
                    </TableRow>
                  ))}
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
            <Stack direction="row" style={{display: "flex", alignItems:"center"}}>
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
                  {files.map((file, index) => (
                    <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                      <TableCell component="th" scope="row">{file}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
            {filename !== "" && !containsTests && (
              <Typography style={{color: 'orange', paddingTop: "20px" }}>
                {t("testWarning")} ⚠️
              </Typography>
            )}
          </Grid>
          <Grid item>
            <TextField
              required
              id="outlined-title"
              label="regex"
              placeholder={t("regexStructure")}
              error={regexError}
              helperText={regexError ? t("helperRegexText") : ''}
              onChange={event => setRegex(event.target.value)}
              onKeyPress={event => handleKeyDown(event)}
            />
          </Grid>
          <Grid item>
            <Button variant="contained" onClick={appendRegex}>
              {t("regex")}
            </Button>
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
                  {regexExpressions.map((regexData: RegexData) => {
                    return (
                      <TableRow key={regexData.key}>
                        <TableCell>{regexData.regex}</TableCell>
                        <TableCell align="right">
                          <IconButton>
                            <DeleteIcon onClick={removeRegex(regexData)}/>
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    )
                  })
                  }
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
          <Grid item>
            <Button variant="contained" onClick={e => {
              return handleSubmit(e);
            }
            }>{t("uploadProject")}</Button>
          </Grid>
        </Grid>
      </FormControl>
    </Box>
  )
}