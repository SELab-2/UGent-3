import {
    Grid,
    Paper,
    Typography,
  } from "@mui/material";
  import { useTranslation } from "react-i18next";
  import {
    Course,    ProjectDetail,
  } from "./CourseUtils";
  import {
    useLoaderData,
  } from "react-router-dom";
  import { Title } from "../Header/Title";
  import { Me } from "../../types/me";
  import {EmptyOrNotProjects} from "./CourseDetailTeacher"
  

  
  /**
   *
   * @returns A jsx component representing the course detail page for a teacher
   */
  export  default function CourseDetailStudent() {


  
    const courseDetail = useLoaderData() as {
      course: Course;
      projects: ProjectDetail[];
      adminMes: Me[];
      studentMes: Me[];
      me:Me;
    };
    const { course, projects, adminMes } = courseDetail;
    const { t } = useTranslation("translation", {
      keyPrefix: "courseDetailTeacher",
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
              <div style={{ padding: "1rem" }}>
                <Typography variant="h5">{t("projects")}:</Typography>
                <EmptyOrNotProjects projects={projects} />
              </div>
            </Paper>
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
            
                      </Grid>
                    ))}
                  </Grid>
                </Paper>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </>
    );
  }
  
  