import { Route, RouterProvider, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
import Layout from "./components/Header/Layout";
import Home from "./pages/home/Home";
import LanguagePath from "./components/LanguagePath";
import ProjectView from "./pages/project/projectView/ProjectView";
import ProjectCreateHome from "./pages/create_project/ProjectCreateHome.tsx";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route index element={<Home />} />
      <Route path=":lang" element={<LanguagePath/>}>
        <Route path="home" element={<Home />} />
        <Route path="project" >
          <Route path=":projectId" element={<ProjectView />}/>
        </Route>
        <Route path="projects">
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
  return (
    <RouterProvider router={router}>
    </RouterProvider>
  );
}