import { Route,RouterProvider, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
import Layout from "./components/Header/Layout";
import { AllCoursesTeacher } from "./components/Courses/AllCoursesTeacher";
import { CourseDetailTeacher } from "./components/Courses/CourseDetailTeacher";
import { loaderCourses } from "./components/Courses/CourseUtils";
import Home from "./pages/home/Home";
import LanguagePath from "./components/LanguagePath";
import ProjectView from "./pages/project/projectView/ProjectView";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route index element={<Home />} />
      <Route path=":lang" element={<LanguagePath/>}>
        <Route path="home" element={<Home />} />
        <Route path="project" >
          <Route path=":projectId" element={<ProjectView />}/>
        </Route>
        <Route path="courses">
          <Route index element={<AllCoursesTeacher />} loader={loaderCourses}/>
          <Route path=":courseId" element={<CourseDetailTeacher />} />
        </Route>
      </Route>
    </Route>
  )
);

/**
 * This component is the main application component that will be rendered by the ReactDOM. 
 * @returns - The main application component
 */
export default function App(): React.JSX.Element {
  return (
    <RouterProvider router={router}>
    </RouterProvider>
  );
}