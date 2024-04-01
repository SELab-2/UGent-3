import { FormControl } from '@mui/base/FormControl';
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
  Typography
} from "@mui/material";
import {ReactNode, useEffect, useState} from "react";
import { spacing } from '@mui/system';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import {LocalizationProvider} from "@mui/x-date-pickers";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";

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
export default function ProjectForm({ setHeaderText }) {

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

  const [testPath, setTestPath] = useState('');

  const [scriptName, setScriptName] = useState('');

  const [regexExpressions, setRegexExpressions] = useState([]);

  const [assignmentFile, setAssignmentFile] = useState<File>();
  const [filename, setFilename] = useState("");

  const [courses, setCourses] = useState<Course[]>([]);
  const [course, setCourse] = useState<Course>({course_id: '', name: "course", teacher: "", ufora_id: ""})
  const [courseId, setCourseId] = useState<string>();
  const [courseName, setCourseName] = useState<string>('')

  const handleFileUpload = async (event) => {
    event.preventDefault();

    if (!event.target.files) {
      return;
    }

    const file = event.target.files[0];
    const { name } = file;
    setAssignmentFile(file)
    setFilename(name);

  }

  const fetchCourses = async () => {
    try {
      const response = await fetch(`${apiUrl}/courses?teacher=${user}`, {
        headers: {
          "Authorization": user
        },
      })
      const jsonData = await response.json();
      setCourses(jsonData.data);
    } catch (e) {
      console.log(e);
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault();

    description == '' ? setDescriptionError(true) : setDescriptionError(false);
    title == '' ? setTitleError(true) : setTitleError(false);

    const formData = new FormData(); // Create FormData object

    // Append fields to the FormData object
    formData.append('title', title);
    formData.append('description', description);
    formData.append('deadline', deadline);
    formData.append('visible_for_students', visibleForStudents);
    formData.append('archived', 'false');
    formData.append('assignment_file', assignmentFile);
    formData.append('course_id', courseId)

    try {
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

    } catch (e) {
      console.log(e);
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
        <Grid item xs={12} sm={6} sx={{ width: '100%' }}>
          <FormControl>
            <InputLabel id="course-select-label">Label werkt niet</InputLabel>
            <Select
              labelId="course-select-label"
              id="demo-simple-select"
              value={courseName}
              label="Course"
              onChange={handleCourseChange}
              fullWidth
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
          <FormControlLabel required control={<Checkbox />} label="Visible for students" />
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
          <Button variant="contained" onClick={ e =>
            handleSubmit(e)
          }>Upload project</Button>
        </Grid>
      </Grid>
    </FormControl>
  )
}