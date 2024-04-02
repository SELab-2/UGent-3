import { BrowserRouter,Route,Routes } from "react-router-dom";
import { Header } from "./components/Header/Header";
import { AllCoursesTeacher, CourseDetailTeacher } from "./components/Courses/Teacher";
import Home from "./pages/home/Home";
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
        <Route path="/courses/:courseId" element={<CourseDetailTeacher />} />
        <Route path="/courses" element={<AllCoursesTeacher />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;