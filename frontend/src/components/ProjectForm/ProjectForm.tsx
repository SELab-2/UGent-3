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
  ListItem, Chip, Stack
} from "@mui/material";
import React, {ChangeEvent, useEffect, useState} from "react";
import {DatePicker} from '@mui/x-date-pickers/DatePicker';
import {LocalizationProvider} from "@mui/x-date-pickers";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import JSZip from 'jszip';
import {useTranslation} from "react-i18next";
import DeleteIcon from "@mui/icons-material/Delete";

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
const user = "teacher1"

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

  const [deadline, setDeadline] = useState<Date>(new Date());

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

  const handleFileUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    event.preventDefault();

    if (!event.target.files) {
      return;
    }

    const file = event.target.files[0];
    const zip = await JSZip.loadAsync(file);

    // Check each file in the zip archive
    let containsTestsFlag = false; // Initialize flag
    for (const [, zipEntry] of Object.entries(zip.files)) {
      if (!zipEntry.dir) {
        // Check if the file is a Dockerfile
        if (zipEntry.name.trim().toLowerCase() === 'dockerfile' || zipEntry.name.trim().toLowerCase() == 'run_tests.sh') {
          containsTestsFlag = true;
        }
      }
    }

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

    const formData = new FormData();

    // Append fields to the FormData object
    formData.append('title', title);
    formData.append('description', description);
    formData.append('deadline', deadline.toISOString());
    formData.append('visible_for_students', visibleForStudents.toString());
    formData.append('archived', 'false');
    formData.append('assignment_file', assignmentFileBlob, filename);
    formData.append('course_id', courseId)
    regexExpressions.forEach((expression,) => {
      formData.append(`regex_expressions`, expression.regex);
    });

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

  const removeRegex = (regexToDelete: RegexData) => () => {
    setRegexExpressions((regexes) => regexes.filter((regex) => regex.key !== regexToDelete.key));
  };

  return (
    <Box
      width='30%'
      paddingLeft='75p'
      paddingBottom='75p'
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
              required
              id="outlined-title"
              label={t("projectDescription")}
              placeholder={t("projectDescription")}
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
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker
                label={t("projectDeadline")}
                disablePast
                onChange={(date: Date | null) => {
                  if (date) {
                    setDeadline(date);
                  }
                }}
                slotProps={{ textField: { helperText: t("helperText") } }}
              />
            </LocalizationProvider>
          </Grid>
          <Grid item>
            <FormControlLabel control={<Checkbox defaultChecked />} label={t("visibleForStudents")} onChange={e=>setVisibleForStudents((e.target as HTMLInputElement).checked)}/>
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              component="label"
            >
              {"Upload file"}
              <input
                type="file"
                hidden
                onChange={e => handleFileUpload(e)}
                accept=".zip,.7zip"
              />
            </Button>
            {filename !== "" && (
              <Typography>{filename}</Typography>
            )}
            {filename !== "" && !containsTests && (
              <Typography style={{ color: 'orange' }}>
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
              helperText={regexError ? "Regex can't be empty or already added" : ''}
              onChange={event => setRegex(event.target.value)}
            />
          </Grid>
          <Grid item>
            <Button variant="contained" onClick={appendRegex}>
              {t("regex")}
            </Button>
          </Grid>
          <Grid item>
            <Stack
              direction="row"
              spacing={1}
            >
              {regexExpressions.map((regexData: RegexData) => {
                return (
                  <ListItem key={regexData.key}>
                    <Chip
                      label={regexData.regex}
                      onDelete={removeRegex(regexData)}
                      deleteIcon={<DeleteIcon />}
                    />
                  </ListItem>
                )
              })
                
              }
            </Stack>
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