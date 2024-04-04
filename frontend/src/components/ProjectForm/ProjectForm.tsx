import {
  Button,
  Checkbox,
  FormControlLabel,
  FormHelperText,
  Grid,
  InputLabel,
  MenuItem, Select, SelectChangeEvent,
  TextField,
  FormControl
} from "@mui/material";
import {ChangeEvent, MouseEvent, useEffect, useState} from "react";
import {DatePicker} from '@mui/x-date-pickers/DatePicker';
import {LocalizationProvider} from "@mui/x-date-pickers";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import JSZip from 'jszip';
import {useTranslation} from "react-i18next";

interface Course {
  course_id: string;
  name: string;
  teacher: string;
  ufora_id: string;
}

const apiUrl = import.meta.env.VITE_APP_API_URL
const user = "teacher1"

/**
 * @returns Form for uploading project
 */
export default function ProjectForm() {

  const { t } = useTranslation('translation', { keyPrefix: 'projectForm' });

  // fix the header value
  useEffect(() => {
    fetchCourses();
  }, []);

  // all the stuff needed for submitting a project
  const [title, setTitle] = useState('');
  const [titleError, setTitleError] = useState(false);

  const [description, setDescription] = useState('');
  const [descriptionError, setDescriptionError] = useState(false);

  // const [assignmentFile, setAssignmentFile] = useState('');

  const [deadline, setDeadline] = useState(new Date());

  const [visibleForStudents, setVisibleForStudents] = useState(false);

  const [regex, setRegex] = useState<string>("");
  const [regexExpressions, setRegexExpressions] = useState<string[]>([]);

  const [assignmentFile, setAssignmentFile] = useState<File>();
  const [filename, setFilename] = useState("");

  const [courses, setCourses] = useState<Course[]>([]);
  const [courseId, setCourseId] = useState<string>('');
  const [courseName, setCourseName] = useState<string>('');

  const [containsTests, setContainsTests] = useState(true);

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
        if (zipEntry.name.trim().toLowerCase() === 'dockerfile') {
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
    const newRegexExpressions = [...regexExpressions, regex];
    setRegexExpressions(newRegexExpressions);
  };

  const handleSubmit = async (event: MouseEvent<HTMLButtonElement, MouseEvent>) => {
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
      formData.append(`regex_expressions`, expression);
    });
    console.log(formData);
    const response = await fetch(apiUrl+"/projects", {
      method: "post",
      headers: {
        "Authorization": user
      },
      body: formData
    })

    if (!response.ok) {
      throw new Error('Network response was not ok');
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

  return (
    <FormControl
      fullWidth
    >
      <Grid
        container
        direction="column"
        justifyContent="center"
        alignItems="center"
        spacing={3}
      >
        <Grid item sx={{ mt: 8 }}>
          <TextField
            required
            id="outlined-title"
            label="title"
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
            placeholder={`Project ${t("projectDescription")}`}
            error={descriptionError}
            onChange={event => setDescription(event.target.value)}
          />
        </Grid>
        <Grid item>
          <FormControl sx={{ width: 246 }}>
            <InputLabel id="demo-simple-select-label">Course</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
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
        <Grid item width={269}>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DatePicker
              label="Project deadline"
              disablePast
              onChange={(date) => {
                setDeadline(date);
              }}
              slotProps={{ textField: { helperText: 'Please fill in a valid deadline for the project' } }}
            />
          </LocalizationProvider>
        </Grid>
        <Grid item>
          <FormControlLabel required control={<Checkbox />} label={t("visibleForStudents")} onChange={e => setVisibleForStudents(e.target.checked)}/>
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
            />
          </Button>
        </Grid>
        {filename !== "" && (
          <Grid item>
            <p>{filename}</p>
          </Grid>
        )}
        {filename !== "" && !containsTests && (
          <Grid item>
            <div style={{ color: 'orange' }}>
              {t("testWarning")} ⚠️
            </div>
          </Grid>
        )}
        <Grid item sx={{ mt: 8 }}>
          <TextField
            required
            id="outlined-title"
            label="regex"
            placeholder="Regex structure"
            error={titleError}
            onChange={event => setRegex(event.target.value)}
            onSubmit={event => appendRegex(event)}
          />
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={appendRegex}>
            {t("regex")}
          </Button>
        </Grid>
        <Grid item>
          <div>
            {regexExpressions.map((expression, index) => (
              <p key={index}>{expression}</p>
            ))}
          </div>
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={e =>
            handleSubmit(e)
          }>Upload project</Button>
        </Grid>
      </Grid>
    </FormControl>
  )
}