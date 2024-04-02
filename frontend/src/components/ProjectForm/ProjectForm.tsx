import {
  Button,
  Checkbox,
  FormControlLabel,
  FormHelperText,
  Grid,
  Input,
  InputLabel,
  MenuItem, Select, SelectChangeEvent,
  TextField,
  Typography,
  FormControl
} from "@mui/material";
import {ChangeEvent, MouseEvent, ReactNode, useEffect, useState} from "react";
import {spacing} from '@mui/system';
import {DatePicker} from '@mui/x-date-pickers/DatePicker';
import {LocalizationProvider} from "@mui/x-date-pickers";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import JSZip from 'jszip';

interface Course {
  course_id: string;
  name: string;
  teacher: string;
  ufora_id: string;
}

/**
 *
 * @param root0
 * @param root0.setHeaderText
 */
const apiUrl = import.meta.env.VITE_APP_API_URL
const user = "teacher1"

/**
 *
 * @param root0
 * @param root0.setHeaderText
 */
export default function ProjectForm({setHeaderText}) {

  // fix the header value
  useEffect(() => {
    // Update header text on page load
    setHeaderText("Project submission form");
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

  const [regexExpressions, setRegexExpressions] = useState([]);

  const [assignmentFile, setAssignmentFile] = useState<File>();
  const [filename, setFilename] = useState("");

  const [courses, setCourses] = useState<Course[]>([]);
  const [course, setCourse] = useState<Course>({course_id: '', name: "course", teacher: "", ufora_id: ""})
  const [courseId, setCourseId] = useState<string>();
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
    for (const [_relativePath, zipEntry] of Object.entries(zip.files)) {
      if (!zipEntry.dir) {
        // Check if the file is a Dockerfile
        if (zipEntry.name.trim().toLowerCase() === 'dockerfile') {
          console.log('Found Dockerfile:', zipEntry.name);
          // Perform actions specific to Dockerfile
          // Example: Extract or process the Dockerfile
          containsTestsFlag = true;
        }
      }
    }

    setContainsTests(containsTestsFlag);
    const {name} = file;
    setAssignmentFile(file)
    setFilename(name);
    console.log(containsTests)

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

  const handleSubmit = async (event: MouseEvent<HTMLButtonElement, MouseEvent>) => {
    event.preventDefault();

    description == '' ? setDescriptionError(true) : setDescriptionError(false);
    title == '' ? setTitleError(true) : setTitleError(false);

    const formData = new FormData(); // Create FormData object

    // Append fields to the FormData object
    formData.append('title', title);
    formData.append('description', description);
    formData.append('deadline', deadline);
    formData.append('visible_for_students', visibleForStudents.toString());
    formData.append('archived', 'false');
    formData.append('assignment_file', assignmentFile);
    formData.append('course_id', courseId)

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
      setCourse(selectedCourse);
      setCourseName(selectedCourse.name);
      setCourseId(selectedCourse.course_id);
    }
  };

  return (
    <FormControl
      onSubmit={handleSubmit}
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
            placeholder="Project title"
            error={titleError}
            onChange={event => setTitle(event.target.value)}
          />
        </Grid>
        <Grid item>
          <TextField
            required
            id="outlined-title"
            label="description"
            placeholder="Project Description"
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
              label="Course"
              onChange={handleCourseChange}
            >
              {courses.map(course => (
                <MenuItem key={course.course_id} value={course.name}>
                  {course.name}
                </MenuItem>
              ))}
            </Select>
            <FormHelperText>Select a course</FormHelperText>
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
          <FormControlLabel required control={<Checkbox />} label="Visible for students" onChange={e => setVisibleForStudents(e.target.checked)}/>
        </Grid>
        <Grid item>
          <Button
            variant="contained"
            component="label"
          >
            Upload File
            <input
              type="file"
              hidden
              onChange={e => handleFileUpload(e)}
            />
          </Button>
        </Grid>
        <Grid item>
          <p>{filename}</p>
        </Grid>
        <Grid item>
          {filename !== "" && !containsTests && (
            <div style={{ color: 'orange' }}>
                Warning: This assignment doesn't contains tests ⚠️
            </div>
          )}
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={ e =>
            handleSubmit(e)
          }>Upload project</Button>
        </Grid>
      </Grid>
    </FormControl>
  )
}