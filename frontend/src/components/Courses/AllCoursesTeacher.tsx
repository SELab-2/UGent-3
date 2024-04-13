import { Button, Dialog, DialogActions, DialogTitle, FormControl, FormHelperText, Grid, Input, InputLabel } from "@mui/material";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import { SideScrollableCourses } from "./CourseUtilComponents";
import { Course, apiHost, loggedInToken, loggedInUid, callToApi } from "./CourseUtils";
import { Title } from "../Header/Title";

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
    <>
      <Title title={t('title')}></Title>
      <Grid container direction={'column'} style={{marginTop: '1rem', width:'100vw', height: '80vh'}}>
        <SideScrollableCourses courses={courses}></SideScrollableCourses>
        <Dialog open={open} onClose={handleClose}>
          <DialogTitle>{t('courseForm')}</DialogTitle>
          <form style={{ margin: "2rem" }} onSubmit={handleSubmit}>
            <FormControl>
              <InputLabel htmlFor="course-name">{t('courseName')}</InputLabel>
              <Input
                id="course-name"
                value={courseName}
                onChange={handleInputChange}
                error={!!error}
                aria-describedby="my-helper-text"
              />
              {error && <FormHelperText id="my-helper-text">{error}</FormHelperText>}
            </FormControl>
            <DialogActions>
              <Button onClick={handleClose}>{t('cancel')}</Button>
              <Button type="submit">{t('submit')}</Button>
            </DialogActions>
          </form>
        </Dialog>
        <Grid item style={{position: "absolute", left: "2rem", bottom: "5rem"}}>
          <Button onClick={handleClickOpen} >{t('create')}</Button>
        </Grid>
      </Grid>
    </>
  );
}