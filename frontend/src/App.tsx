import { Route, RouterProvider, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
import Layout from "./components/Header/Layout";
import { AllCoursesTeacher } from "./components/Courses/AllCoursesTeacher";
import { CourseDetailTeacher } from "./components/Courses/CourseDetailTeacher";
import { dataLoaderCourseDetail, dataLoaderCourses } from "./components/Courses/CourseUtils";
import LanguagePath from "./components/LanguagePath";
import ProjectView from "./pages/project/projectView/ProjectView";
import { ErrorBoundary } from "./pages/error/ErrorBoundary.tsx";
import ProjectCreateHome from "./pages/create_project/ProjectCreateHome.tsx";
import SubmissionsOverview from "./pages/submission_overview/SubmissionsOverview.tsx";
import {fetchProjectPage} from "./utils/fetches/FetchProjects.tsx";
import HomePages from "./pages/home/HomePages.tsx";
import ProjectOverView from "./pages/project/projectOverview.tsx";
import {fetchMe} from "./utils/fetches/FetchMe.ts";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />} errorElement={<ErrorBoundary />} loader={fetchMe}>
      <Route index element={<HomePages />} loader={fetchProjectPage}/>
      <Route path=":lang" element={<LanguagePath/>}>
        <Route path="home" element={<HomePages />} loader={fetchProjectPage} />
        <Route path="project/:projectId/overview" element={<SubmissionsOverview/>}/>
        <Route path="project">
          <Route path=":projectId" element={<ProjectView />}>
          </Route>
        </Route>
        <Route path="courses">
          <Route index element={<AllCoursesTeacher />} loader={dataLoaderCourses}/>
          <Route path=":courseId" element={<CourseDetailTeacher />} loader={dataLoaderCourseDetail} />
        </Route>
        <Route path="projects">
          <Route index element={<ProjectOverView/>} loader={fetchProjectPage}/>
          <Route path="create" element={<ProjectCreateHome />} />
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
  return <RouterProvider router={router} />;
}
