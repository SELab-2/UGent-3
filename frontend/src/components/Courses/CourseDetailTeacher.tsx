import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Checkbox,
  FormControlLabel,
  Grid,
  IconButton,
  Input,
  InputLabel,
  Menu,
  MenuItem,
  Paper,
  Tooltip,
  Typography,
} from "@mui/material";
import { ChangeEvent, useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Course,
  apiHost,
  getIdFromLink,
  getNearestFutureDate,
  ProjectDetail,
} from "./CourseUtils";
import {
  Link,
  useNavigate,
  NavigateFunction,
  useLoaderData,
} from "react-router-dom";
import { Title } from "../Header/Title";
import ClearIcon from "@mui/icons-material/Clear";
import { timeDifference } from "../../utils/date-utils";
import { authenticatedFetch } from "../../utils/authenticated-fetch";
import i18next from "i18next";
import { Me } from "../../types/me";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

interface UserUid {
  uid: string;
}

/**
 * Handles the deletion of an admin.
 * @param navigate - The navigate function from react-router-dom.
 * @param courseId - The ID of the course.
 * @param uid - The UID of the admin.
 */
function handleDeleteAdmin(
  navigate: NavigateFunction,
  courseId: string,
  uid: string
): void {
  authenticatedFetch(`${apiHost}/courses/${courseId}/admins`, {
    method: "DELETE",
    body: JSON.stringify({
      admin_uid: uid,
    }),
  }).then(() => {
    navigate(0);
  });
}

/**
 * Handles the deletion of a student.
 * @param navigate - The navigate function from react-router-dom.
 * @param courseId - The ID of the course.
 * @param uid - The UID of the admin.
 */
function handleDeleteStudent(
  navigate: NavigateFunction,
  courseId: string,
  uids: string[]
): void {
  authenticatedFetch(`${apiHost}/courses/${courseId}/students`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      students: uids,
    }),
  }).then(() => {
    navigate(0);
  });
}

/**
 * Handles the deletion of a course.
 * @param navigate - The navigate function from react-router-dom.
 * @param courseId - The ID of the course.
 */
function handleDeleteCourse(
  navigate: NavigateFunction,
  courseId: string
): void {
  authenticatedFetch(`${apiHost}/courses/${courseId}`, {
    method: "DELETE",
  }).then((response) => {
    if (response.ok) {
      navigate(-1);
    } else if (response.status === 404) {
      navigate(-1);
    }
  });
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
    course: Course;
    projects: ProjectDetail[];
    adminMes: Me[];
    studentMes: Me[];
  };
  const { course, projects, adminMes, studentMes } = courseDetail;
  const { t } = useTranslation("translation", {
    keyPrefix: "courseDetailTeacher",
  });

  const { i18n } = useTranslation();
  const lang = i18n.language;
  const navigate = useNavigate();

  const handleCheckboxChange = (
    event: ChangeEvent<HTMLInputElement>,
    uid: string
  ) => {
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
      <Title title={course.name}></Title>
      <Grid
        container
        direction={"row"}
        spacing={2}
        margin="1rem"
        style={{ height: "80vh" }}
      >
        <Grid item xs={5} height="100%">
          <Paper
            style={{ height: "100%", maxHeight: "100%", overflow: "auto" }}
          >
            <div style={{ padding: "1rem" }}>
              <Typography variant="h5">{t("projects")}:</Typography>
              <EmptyOrNotProjects projects={projects} />
            </div>
          </Paper>
          <Link to={`/${lang}/projects/create?course_id=${course.course_id}`}>
            <Button>{t("newProject")}</Button>
          </Link>
        </Grid>
        <Grid item xs={5} height="100%">
          <Grid container direction={"column"} spacing={2} height={"100%"}>
            <Grid
              item
              style={{
                height: "50%",
              }}
            >
              <Paper
                style={{
                  overflow: "auto",
                  height: "100%",
                }}
              >
                <Typography variant="h5">{t("admins")}:</Typography>
                <Grid container direction={"column"}>
                  {adminMes.map((admin: Me) => (
                    <Grid
                      container
                      alignItems="center"
                      spacing={1}
                      key={admin.uid}
                    >
                      <Grid item>
                        <Typography variant="body1">
                          {admin.display_name}
                        </Typography>
                      </Grid>
                      <EitherDeleteIconOrNothing
                        admin={admin}
                        course={course}
                        navigate={navigate}
                      />
                    </Grid>
                  ))}
                </Grid>
              </Paper>
            </Grid>
            <Grid
              item
              style={{
                height: "50%",
              }}
            >
              <Paper
                style={{
                  maxHeight: "100%",
                  overflow: "auto",
                }}
              >
                <Typography variant="h5">{t("students")}:</Typography>
                <EmptyOrNotStudents
                  students={studentMes}
                  selectedStudents={selectedStudents}
                  handleCheckboxChange={handleCheckboxChange}
                />
              </Paper>
              <Grid container>
                <Grid item>
                  <Button onClick={handleClickCodes}>{t("joinCodes")}</Button>
                  <JoinCodeMenu
                    courseId={course.course_id}
                    open={openCodes}
                    handleClose={handleCloseCodes}
                    anchorEl={anchorEl}
                  />
                </Grid>
                <Grid item>
                  <Button
                    onClick={() =>
                      handleDeleteCourse(navigate, course.course_id)
                    }
                  >
                    {t("deleteCourse")}
                  </Button>
                </Grid>
              </Grid>

              <IconButton
                style={{ position: "absolute", bottom: 0, left: 0 }}
                onClick={() =>
                  handleDeleteStudent(
                    navigate,
                    course.course_id,
                    selectedStudents
                  )
                }
              >
                <ClearIcon />
                <Typography variant="body1">{t("deleteSelected")}</Typography>
              </IconButton>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
}

/**
 * @param projects - The array of projects.
 * @returns Either a place holder for no projects or a grid of cards describing the projects.
 */
function EmptyOrNotProjects({
  projects,
}: {
  projects: ProjectDetail[];
}): JSX.Element {
  const { t } = useTranslation("translation", {
    keyPrefix: "courseDetailTeacher",
  });
  if (projects === undefined || projects.length === 0) {
    return <Typography variant="h6">{t("noProjects")}</Typography>;
  } else {
    return (
      <Grid
        container
        direction={"row"}
        spacing={3}
        style={{
          display: "flex",
          flexWrap: "wrap",
          marginTop: "1rem",
        }}
      >
        {projects?.map((project) => (
          <Grid item sm={6} key={project.project_id}>
            <Card style={{ background: "lightblue" }} key={project.project_id}>
              <Link
                to={`/${i18next.language}/projects/${getIdFromLink(project.project_id)}`}
              >
                <CardHeader title={project.title} />
              </Link>
              <CardContent>
                {getNearestFutureDate(project.deadlines) && (
                  <Typography variant="body1">
                    {`${t("deadline")}: ${getNearestFutureDate(project.deadlines)?.date.toLocaleDateString()}`}
                  </Typography>
                )}
              </CardContent>
              <CardActions>
                <Link
                  to={`/${i18next.language}/projects/${getIdFromLink(project.project_id)}`}
                >
                  <Button>{t("view")}</Button>
                </Link>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  }
}

/**
 * @param navigate - The navigate function from react-router-dom.
 * @param course - The course against which we will check if the uid is of the teacher.
 * @param admin - The admin in question.
 * @returns Either nothing, if the admin uid is of teacher or a delete button.
 */
function EitherDeleteIconOrNothing({
  admin,
  course,
  navigate,
}: {
  admin: UserUid;
  course: Course;
  navigate: NavigateFunction;
}): JSX.Element {
  if (course.teacher === getIdFromLink(admin.uid)) {
    return <></>;
  } else {
    return (
      <Grid item>
        <IconButton
          onClick={() =>
            handleDeleteAdmin(
              navigate,
              course.course_id,
              getIdFromLink(admin.uid)
            )
          }
        >
          <ClearIcon />
        </IconButton>
      </Grid>
    );
  }
}

/**
 * @param students - The array of students.
 * @param selectedStudents - The array of selected students.
 * @param handleCheckboxChange - The function to handle the checkbox change.
 * @returns Either a place holder for no students or a grid of checkboxes for the students.
 */
function EmptyOrNotStudents({
  students,
  selectedStudents,
  handleCheckboxChange,
}: {
  students: Me[];
  selectedStudents: string[];
  handleCheckboxChange: (
    event: React.ChangeEvent<HTMLInputElement>,
    studentId: string
  ) => void;
}): JSX.Element {
  if (students.length === 0) {
    return (
      <Typography
        variant="h6"
        style={{ marginLeft: "5rem", marginTop: "2rem" }}
      >
        No students found
      </Typography>
    );
  } else {
    return (
      <Grid container direction="column">
        {students.map((student) => (
          <Grid
            item
            container
            alignItems="center"
            spacing={1}
            key={student.uid}
          >
            <Grid item>
              <Checkbox
                checked={selectedStudents.includes(getIdFromLink(student.uid))}
                onChange={(event) =>
                  handleCheckboxChange(event, getIdFromLink(student.uid))
                }
              />
            </Grid>
            <Grid item>
              <Typography variant="body1">{student.display_name}</Typography>
            </Grid>
          </Grid>
        ))}
      </Grid>
    );
  }
}

interface JoinCode {
  join_code: string;
  expiry_time: string;
  for_admins: boolean;
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
function JoinCodeMenu({
  courseId,
  open,
  handleClose,
  anchorEl,
}: {
  courseId: string;
  open: boolean;
  handleClose: () => void;
  anchorEl: HTMLElement | null;
}) {
  const { t } = useTranslation("translation", {
    keyPrefix: "courseDetailTeacher",
  });

  const [codes, setCodes] = useState<JoinCode[]>([]);
  const [expiry_time, setExpiryTime] = useState<Date | null>(null);
  const [for_admins, setForAdmins] = useState<boolean>(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setExpiryTime(new Date(event.target.value));
  };

  const handleCopyToClipboard = (join_code: string) => {
    const host = window.location.host;
    navigator.clipboard.writeText(
      `${host}/${i18next.language}/courses/join?code=${join_code}`
    );
  };

  const getCodes = useCallback(() => {
    authenticatedFetch(`${apiHost}/courses/${courseId}/join_codes`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        const filteredData = data.data.filter((code: JoinCode) => {
          // Filter out expired codes
          let expired = false;
          if (code.expiry_time !== null) {
            const expiryTime = new Date(code.expiry_time);
            const now = new Date();
            expired = expiryTime < now;
          }

          return !expired;
        });
        setCodes(filteredData);
      });
  }, [courseId]);

  const handleNewCode = () => {
    const bodyContent: { for_admins: boolean; expiry_time?: string } = {
      for_admins: for_admins,
    };
    if (expiry_time !== null) {
      bodyContent.expiry_time = expiry_time.toISOString();
    }

    authenticatedFetch(`${apiHost}/courses/${courseId}/join_codes`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bodyContent),
    }).then(() => getCodes());
  };

  const handleDeleteCode = (joinCode: string) => {
    authenticatedFetch(
      `${apiHost}/courses/${courseId}/join_codes/${joinCode}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          join_code: joinCode,
        }),
      }
    ).then(() => getCodes());
  };

  useEffect(() => {
    getCodes();
  }, [t, getCodes]);

  return (
    <Box>
      <Menu
        open={open}
        onClose={handleClose}
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "center",
        }}
        transformOrigin={{
          vertical: "bottom",
          horizontal: "center",
        }}
        style={{
          width: "25vw",
        }}
      >
        <MenuItem disabled>
          <Typography variant="h6">{t("joinCodes")}</Typography>
        </MenuItem>
        <Paper
          elevation={0}
          style={{
            margin: "1rem",
            width: "100%",
            maxHeight: "20vh",
            height: "20vh",
            overflowY: "auto",
          }}
        >
          {codes.map((code: JoinCode) => (
            <MenuItem style={{ width: "100%" }} key={code.join_code}>
              <Grid container direction={"row"}>
                <Grid item flexGrow={1}>
                  <Box display="flex" gap="1rem">
                    <Typography variant="body1">
                      {code.expiry_time
                        ? timeDifference(code.expiry_time)
                        : t("noExpiryDate")}
                    </Typography>
                    <Typography variant="body1">
                      {code.for_admins ? t("forAdmins") : t("forStudents")}
                    </Typography>
                    <Tooltip title={t("copyToClipboard")}>
                      <IconButton
                        onClick={() => handleCopyToClipboard(code.join_code)}
                      >
                        <ContentCopyIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
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
        <MenuItem style={{ marginTop: "1rem" }}>
          <InputLabel htmlFor="expiry-date" style={{ marginRight: "1rem" }}>
            {t("expiryDate")}:{" "}
          </InputLabel>
          <Input
            id="expiry-date"
            type="date"
            value={
              expiry_time ? expiry_time.toISOString().substring(0, 10) : ""
            }
            onChange={handleInputChange}
            style={{ marginRight: "2rem" }}
          />
          <FormControlLabel
            label={t("forAdmins")}
            control={
              <Checkbox
                checked={for_admins}
                onChange={(event) => setForAdmins(event.target.checked)}
                name="forAdmins"
                color="primary"
              />
            }
          />
          <Button onClick={handleNewCode}>{t("newJoinCode")}</Button>
        </MenuItem>
      </Menu>
    </Box>
  );
}
