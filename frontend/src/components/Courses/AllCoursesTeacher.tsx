import { Button, Dialog, DialogActions, DialogTitle, FormControl, FormLabel, Grid, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { SideScrollableCourses } from "./CourseUtilComponents";
import { Course, apiHost, loggedInToken, loggedInUid, callToApi } from "./CourseUtils";

/**
 * @returns A jsx component representing all courses for a teacher
 */
export function AllCoursesTeacher(): JSX.Element {
  const [courses, setActiveCourses] = useState<Course[]>([]);
  const [open, setOpen] = useState(false);

  const [courseName, setCourseName] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const { t } = useTranslation('translation', { keyPrefix: 'allCoursesTeacher' });
  
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  useEffect(() => {
    const params = new URLSearchParams({ teacher: loggedInUid() });
    fetch(`${apiHost}/courses?${params}`, {
      headers: {
        "Authorization": loggedInToken()
      }
    })
      .then(response => response.json())
      .then(data => {
        setActiveCourses(data.data);
      })
      .catch(error => console.error('Error:', error));
  }, []);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCourseName(event.target.value);
    setError(''); // Clearing error message when user starts typing
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevents the default form submission behaviour

    if (!courseName.trim()) {
      setError(t('emptyCourseNameError'));
      return;
    }

    const data = { name: courseName };
    callToApi(`${apiHost}/courses`, JSON.stringify(data), 'POST', navigate);
  };

  return (
    <Grid container direction={'column'} style={{marginTop: '20px'}}>
      <SideScrollableCourses courses={courses}></SideScrollableCourses>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{t('courseForm')}</DialogTitle>
        <form style={{margin:"2rem"}} onSubmit={handleSubmit}>
          <FormControl>
            <FormLabel htmlFor="course-name">{t('courseName')}</FormLabel>
            <TextField
              value={courseName}
              onChange={handleInputChange}
              error={!!error} // Applying error style if there's an error message
              helperText={error} // Displaying the error message
              sx={{ borderColor: error ? 'red' : undefined }} // Changing border color to red if there's an error
            />
          </FormControl>
          <DialogActions>
            <Button onClick={handleClose}>{t('cancel')}</Button>
            <Button type="submit">{t('submit')}</Button>
          </DialogActions>
        </form> 
      </Dialog>
      <Grid item style={{marginLeft:"2rem", marginTop:"2rem"}}>
        <Button onClick={handleClickOpen} >{t('create')}</Button>
      </Grid>
    </Grid>
  );
}