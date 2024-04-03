import { BrowserRouter,Route,Routes } from "react-router-dom";
import { Header } from "./components/Header/Header";
import ProjectCreateHome from "./pages/create_project/ProjectCreateHome.tsx";

import Home from "./pages/home/Home";
/**
 * This component is the main application component that will be rendered by the ReactDOM. 
 * @returns - The main application component
 */
function App(): JSX.Element {

  return (
    <BrowserRouter>
      <Header/>
      <Routes>
        <Route index element={<Home />} />
        <Route path="dummy-create-project" element={<ProjectCreateHome />}/>
      </Routes>
    </BrowserRouter>
  );
}
export default App;