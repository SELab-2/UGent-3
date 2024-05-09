import { 
  Grid, 
  Paper, 
  Typography 
} from "@mui/material";
import { useLoaderData } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Course } from "../../types/course";
import { ProjectDetail } from "./CourseUtils";
import { Title } from "../Header/Title";
import { EmptyOrNotProjects } from "./CourseDetailTeacher";

/**
 *
 * @returns The component representing the course details page for a student.
 */
export function CourseDetailStudent(): JSX.Element {
  const courseDetail = useLoaderData() as {
    course: Course;
    projects: ProjectDetail[];
  };

  const { course, projects } = courseDetail;
  const { t } = useTranslation("translation", {
    keyPrefix: "courseDetail",
  });

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
            <Typography variant="h5">{t("projects")}:</Typography>
            <EmptyOrNotProjects projects={projects} />
          </Paper>
        </Grid>
      </Grid>
    </>
  );
}
