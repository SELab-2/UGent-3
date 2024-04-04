import { BrowserRouter, Route, Routes } from "react-router-dom";
import HomeStudent from "./pages/home/Home_student.tsx";
import Home from "./pages/home/Home.tsx"
import { Header } from "./components/Header/Header";

/**
 * This component is the main application component that will be rendered by the ReactDOM.
 * @returns - The main application component
 */
function App(): JSX.Element {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Home />} />// no header on the homepage
        <Route path="/*" element={// Pages with header
          <><Header />
            <Routes>
              <Route path="/student" element={<HomeStudent />} />
            </Routes></>
        }/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
