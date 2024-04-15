import { Box, Button, Card, CardActions, CardContent, CardHeader, Checkbox, FormControlLabel, Grid, IconButton, Input, Menu, MenuItem, Paper, Typography } from "@mui/material";
import { ChangeEvent, useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Course, Project, apiHost, loggedInToken, getIdFromLink, getNearestFutureDate, getUserName } from "./CourseUtils";
import { Link, useNavigate, NavigateFunction, useLoaderData } from "react-router-dom";
import { Title } from "../Header/Title";
import ClearIcon from '@mui/icons-material/Clear';
import { timeDifference } from "../../utils/date-utils";

interface UserUid{
    uid: string
}

/**
 * Handles the deletion of an admin.
 * @param navigate - The navigate function from react-router-dom.
 * @param courseId - The ID of the course.
 * @param uid - The UID of the admin.
 */
function handleDeleteAdmin(navigate: NavigateFunction, courseId: string, uid: string): void {
  fetch(`${apiHost}/courses/${courseId}/admins`, {
    method: 'DELETE',
    headers: {
      "Authorization": loggedInToken(),
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "admin_uid": uid
    })
  })
    .then(() => {
      navigate(0);
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Handles the deletion of a student.
 * @param navigate - The navigate function from react-router-dom.
 * @param courseId - The ID of the course.
 * @param uid - The UID of the admin.
 */
function handleDeleteStudent(navigate: NavigateFunction, courseId: string, uids: string[]): void {
  fetch(`${apiHost}/courses/${courseId}/students`, {
    method: 'DELETE',
    headers: {
      "Authorization": loggedInToken(),
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "students": uids
    })
  })
    .then(() => {
      navigate(0);
    })
    .catch(error => console.error('Error:', error));
}
/**
 * 
 * @returns A jsx component representing the course detail page for a teacher
 */
export function CourseDetailTeacher(): JSX.Element {
  const [selectedStudents, setSelectedStudents] = useState<string[]>([]);
  const [anchorEl, setAnchorElStudent] = useState<null | HTMLElement>(null);
  const openCodes = Boolean(anchorEl);

  const handleClickCodes = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorElStudent(event.currentTarget);
  };
  const handleCloseCodes = () => {
    setAnchorElStudent(null);
  };

  const courseDetail = useLoaderData() as {
    course: Course ,
    projects:Project[] ,
    admins: UserUid[],
    students: UserUid[]
  };
  const { course, projects, admins, students } = courseDetail;

  const { t } = useTranslation('translation', { keyPrefix: 'courseDetailTeacher' });
  const { i18n } = useTranslation();
  const lang = i18n.language;
  const navigate = useNavigate();

  const handleCheckboxChange = (event: ChangeEvent<HTMLInputElement>, uid: string) => {
    if (event.target.checked) {
      setSelectedStudents((prevSelected) => [...prevSelected, uid]);
    } else {
      setSelectedStudents((prevSelected) =>
        prevSelected.filter((student) => student !== uid)
      );
    }
  };
    
  return (
    <>
      <Title title={t('title')}></Title>
      <Grid container margin={"1rem"} direction={"column"}>
        <Grid item marginBottom={"0.5rem"}>
          <Typography variant="h4">{course.name}</Typography>
        </Grid>
        <Grid item>
          <Grid container direction={"row"}>
            <Grid item style={{ width: "50%" }}>
              <Paper elevation={0} style={{ height:"70vh", maxHeight:"70vh", overflowY:"auto"}}>
                <Typography variant="h5">{t('projects')}:</Typography>
                <Grid container direction={"row"}>
                  {projects?.map((project) => (
                    <Grid item key={project.project_id} margin={"2rem"}>
                      <Card style={{ background: "lightblue" }} key={project.project_id}>
                        <Link to={`/projects/${getIdFromLink(project.project_id)}`}>
                          <CardHeader title={project.title} />
                        </Link>
                        <CardContent>
                          {getNearestFutureDate(project.deadlines) &&
                            (
                              <Typography variant="body1">
                                {`${t('deadline')}: ${getNearestFutureDate(project.deadlines)?.toLocaleDateString()}`}
                              </Typography>
                            )}
                        </CardContent>
                        <CardActions>
                          <Link to={`/projects/${project.project_id}`}>
                            <Button>{t('view')}</Button>
                          </Link>
                        </CardActions>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Paper>
              <Link to={`/${lang}/projects/create?course_id=${course.course_id}`}><Button>{t('newProject')}</Button></Link>
            </Grid>
            <Grid item style={{ marginLeft: "1rem" }}>
              <Grid container direction={"column"}>
                <Grid item position={"relative"} height={"35vh"} width={"35vw"}>
                  <Paper elevation={0} style={{maxHeight:"35vh", overflowY:"auto"}}>
                    <Typography variant="h5">{t('admins')}:</Typography>
                    <Grid container direction={"column"}>
                      {admins.map((admin) => (
                        <Grid item container alignItems="center" spacing={1} key={admin.uid}>
                          <Grid item>
                            <Typography variant="body1">{getUserName(admin.uid)}</Typography>
                          </Grid>
                          <Grid item>
                            <IconButton onClick={() => handleDeleteAdmin(navigate,course.course_id,getIdFromLink(admin.uid))}>
                              <ClearIcon />
                            </IconButton>
                          </Grid>
                        </Grid>
                      ))}
                    </Grid>
                  </Paper>
                </Grid>
                <Grid item position={"relative"} height={"35vh"} width={"35vw"}>
                  <Typography variant="h5">{t('students')}:</Typography>
                  <Paper elevation={0} style={{maxHeight:"25vh", overflowY:"auto"}}>
                    <Grid container direction="column">
                      {students.map((student) => (
                        <Grid item container alignItems="center" spacing={1} key={student.uid}>
                          <Grid item>
                            <Checkbox
                              checked={selectedStudents.includes(getIdFromLink(student.uid))}
                              onChange={(event) => handleCheckboxChange(event, getIdFromLink(student.uid))}
                            />
                          </Grid>
                          <Grid item>
                            <Typography variant="body1">{getUserName(student.uid)}</Typography>
                          </Grid>
                        </Grid>
                      ))}
                    </Grid>
                  </Paper>
                  <IconButton style={{ position: "absolute", bottom:0, left:0}} onClick={() => handleDeleteStudent(navigate, course.course_id, selectedStudents)}>
                    <ClearIcon />
                    <Typography variant="body1">{t('deleteSelected')}</Typography>
                  </IconButton>
                </Grid>
                <Grid item>
                  <Button onClick={handleClickCodes}>{t('joinCodes')}</Button>
                  <JoinCodeMenu courseId={course.course_id} open={openCodes} handleClose={handleCloseCodes} anchorEl={anchorEl}/>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </>
  );

}

interface JoinCode{
  join_code: string,
  expiry_time: string,
  for_admins: boolean
}

/**
 * Renders the JoinCodeMenu component.
 * @param open - Whether the dialog is open or not.
 * @param handleClose - Function to handle the dialog close event.
 * @param handleNewCode - Function to handle the creation of a new join code.
 * @param handleDeleteCode - Function to handle the deletion of a join code.
 * @param getCodes - Function to get the list of join codes.
 * @returns The rendered JoinCodeDialog component.
 */
function JoinCodeMenu({courseId,open,handleClose, anchorEl}: {courseId:string, open: boolean, handleClose : () => void, anchorEl: HTMLElement | null}) {
  const { t } = useTranslation('translation', { keyPrefix: 'courseDetailTeacher' });

  const [codes, setCodes] = useState<JoinCode[]>([]);
  const [expiry_time, setExpiryTime] = useState<Date | null>(null);
  const [for_admins, setForAdmins] = useState<boolean>(false);
  
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setExpiryTime(new Date(event.target.value));
  };

  const handleCopyToClipboard = (join_code: string) => {
    navigator.clipboard.writeText(`${apiHost}/join-course?code=${join_code}`)
      .catch((error) => {
        console.error('Error copying text to clipboard:', error);
      });
  };

  const getCodes = useCallback(() => {
    fetch(`${apiHost}/courses/${courseId}/join_codes`, {
      method: 'GET',
      headers: {
        'Authorization': loggedInToken()
      }
    })
      .then(response => response.json())
      .then(data => {
        const filteredData = data.data.filter((code: JoinCode) => {
          // Filter out expired codes and codes not for admins if for_admins is true
          let expired = false;
          if(code.expiry_time !== null){
            const expiryTime = new Date(code.expiry_time);
            const now = new Date();
            expired = expiryTime < now;
          }
          
          return !expired;
        });
        setCodes(filteredData);
      })
      .catch(error => console.error('Error:', error));
  }, [courseId])

  const handleNewCode = () => {
    
    const bodyContent: { for_admins: boolean, expiry_time?: string } = { "for_admins": for_admins };
    if (expiry_time !== null) {
      bodyContent.expiry_time = expiry_time.toISOString();
    }

    fetch(`${apiHost}/courses/${courseId}/join_codes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': loggedInToken()
      },
      body: JSON.stringify(bodyContent)
    })
      .then(() => getCodes())
      .catch(error => console.error('Error:', error));
  }

  const handleDeleteCode = (joinCode: string) => {
    fetch(`${apiHost}/courses/${courseId}/join_codes/${joinCode}`,
      {
        method: 'DELETE',
        headers: {
          "Authorization": loggedInToken(),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "join_code": joinCode
        })
      })
      .then(() => getCodes())
      .catch(error => console.error('Error:', error));
  }

  useEffect(() => {
    getCodes();
  }, [t, getCodes ]);

  return (
    <Box>
      <Menu 
        open={open} 
        onClose={handleClose} 
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
      >
        <MenuItem disabled>
          <Typography variant="h6">{t('joinCodes')}</Typography>
        </MenuItem>
        <Paper elevation={0} style={{margin:"1rem", width:"30vw" ,maxHeight: "20vh", height: "20vh", overflowY:"auto" }}>
          {codes.map((code:JoinCode) => (
            <MenuItem onClick={() => handleCopyToClipboard(code.join_code)} key={code.join_code}>
              <Grid container direction={"row"}>
                <Grid width={"7vw"} marginRight={"1rem"} item>
                  <Typography variant="body1">{code.expiry_time ? timeDifference(code.expiry_time) : t('noExpiryDate')}</Typography>
                </Grid>
                <Grid item width={"7vw"}>
                  <Typography variant="body1">{code.for_admins ? t('forAdmins') : t('forStudents')}</Typography>
                </Grid>
                <Grid item>
                  <IconButton onClick={() => handleDeleteCode(code.join_code)}>
                    <ClearIcon />
                  </IconButton>
                </Grid>
              </Grid>
            </MenuItem>
          ))}
        </Paper>
        <MenuItem style={{marginTop:"1rem"}}>
          <Input
            id="expiry-date"
            type="datetime-local"
            value={expiry_time ? expiry_time.toISOString().substring(0, 16) : ''}
            onChange={handleInputChange}
            style={{marginRight:"2rem"}}
          />
          <FormControlLabel
            label={t('forAdmins')}
            control={
              <Checkbox
                checked={for_admins}
                onChange={(event) => setForAdmins(event.target.checked)}
                name="forAdmins"
                color="primary"
              />
            }
          />
          <Button onClick={handleNewCode}>{t('newJoinCode')}</Button>
        </MenuItem>
      </Menu>
    </Box>
  );
}