import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/home/Home";
import { Header } from "./components/Header/Header";
import { CourseForm } from "./components/Courses/CourseForm";
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
        <Route path="/courses/create" element={<CourseForm />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
