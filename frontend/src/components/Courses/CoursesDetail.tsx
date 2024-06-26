import {useLoaderData} from "react-router-dom";
import {Me} from "../../types/me.ts";
import {Course, ProjectDetail} from "./CourseUtils.tsx";
import CourseDetailTeacher from "./CourseDetailTeacher.tsx";
import CourseDetailStudent from "./CourseDetailStudent.tsx";

/**
 * gives the right detail page
 * @returns - detail page
 */
export default function CoursesDetail() :JSX.Element {
  const loader = useLoaderData() as {
    course: Course;
    projects: ProjectDetail[];
    adminMes: Me[];
    studentMes: Me[];
    me:Me;
  };
  if (loader.course.teacher === loader.me.uid) {
    return <CourseDetailTeacher/>;
  } else {
    return <CourseDetailStudent/>;
  }
}