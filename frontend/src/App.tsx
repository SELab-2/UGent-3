import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomeStudent from "./pages/home/Home_student.tsx";
import { Header } from "./components/Header/Header";

/**
 * This component is the main application component that will be rendered by the ReactDOM. 
 * @returns - The main application component
 */
function App(): JSX.Element {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route index element={<HomeStudent />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
