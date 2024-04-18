import { Route, RouterProvider, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
import Layout from "./components/Header/Layout";
import LanguagePath from "./components/LanguagePath";
import ProjectView from "./pages/project/projectView/ProjectView";
import { ErrorBoundary } from "./pages/error/ErrorBoundary.tsx";
import ProjectCreateHome from "./pages/create_project/ProjectCreateHome.tsx";
import {fetchProjectPage} from "./pages/project/FetchProjects.tsx";
import HomePages from "./pages/home/HomePages.tsx";
import ProjectOverView from "./pages/project/projectOverview.tsx";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />} errorElement={<ErrorBoundary />}>
      <Route index element={<HomePages />} loader={fetchProjectPage}/>
      <Route path=":lang" element={<LanguagePath/>}>
        <Route path="home" element={<HomePages />} loader={fetchProjectPage} />
        <Route path="project" >
          <Route path=":projectId" element={<ProjectView />}/>
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
