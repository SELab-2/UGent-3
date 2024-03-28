import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/home/Home";
import { Header } from "./components/Header/Header";
import ProjectCreateHome from "./pages/create_project/ProjectCreateHome.tsx";
import {useState} from "react";

/**
 * This component is the main application component that will be rendered by the ReactDOM. 
 * @returns - The main application component
 */
function App(): JSX.Element {
  const [headerText, setHeaderText] = useState("Home");

  return (
    <BrowserRouter>
      <Header headerText={headerText}/>
      <Routes>
        <Route index element={<Home />} />
        <Route path="dummy-create-project" element={<ProjectCreateHome setHeaderText={setHeaderText} />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
