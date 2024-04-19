import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

import { Course } from "../../types/course";
import { Project } from "../../types/project";
import { Box, Typography } from "@mui/material";

const API_URL = import.meta.env.VITE_API_HOST;

export default function CourseDetails() {
  const { courseId } = useParams<{ courseId: string }>();
  const [courseData, setCourseData] = useState<Course | null>(null);
  const [projects, setProjects] = useState<Project[] | []>([]);

  useEffect(() => {
    fetch(`${API_URL}/courses/${courseId}`, {
      headers: { Authorization: "student" },
      credentials: "include"
    }).then((response) => {
      if (response.ok) {
        response.json().then((json) => {
          setCourseData(json["data"]);
        });
      }
    });

    courseData?.projects.forEach((projectId) => {
      fetch(`${API_URL}/courses/${projectId}`, {
        headers: { Authorization: "student" },
        credentials: "include"
      }).then((response) => {
        if (response.ok) {
          response.json().then((json) => {
            setProjects([...projects, json["data"]]);
          });
        }
      });
    });
  }, [courseId]);

  return (
    <>
      <Box>
        <Typography>
          {courseData?.name}
        </Typography>
        <Typography>
          {projects[0].title}
        </Typography>
      </Box>
    </>
  )
}