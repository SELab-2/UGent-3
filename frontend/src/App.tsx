import { BrowserRouter,Route,Routes } from "react-router-dom";
import { Header } from "./components/Header/Header";
import { AllCoursesTeacher } from "./components/Courses/AllCoursesTeacher";
import { CourseDetailTeacher } from "./components/Courses/CourseDetailTeacher";
import Home from "./pages/home/Home";
import LanguagePath from "./components/LanguagePath";
import ProjectView from "./pages/project/projectView/ProjectView";

/**
 * This component is the main application component that will be rendered by the ReactDOM. 
 * @returns - The main application component
 */
function App(): JSX.Element {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route index element={<Home />} />
        <Route path=":lang" element={<LanguagePath/>}>
          <Route path="home" element={<Home />} />
          <Route path="project" >
            <Route path=":projectId" element={<ProjectView />}/>
          </Route>
          <Route path="courses">
            <Route index element={<AllCoursesTeacher />} />
            <Route path=":courseId" element={<CourseDetailTeacher />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
export default App;