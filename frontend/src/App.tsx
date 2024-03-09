import { BrowserRouter } from "react-router-dom";
import Navbar from "./components/Header/Navbar";

/**
 * This component is the main application component that will be rendered by the ReactDOM. 
 * @returns - The main application component
 */
function App(): JSX.Element {
  return (
    <BrowserRouter>
      <Navbar/>
    </BrowserRouter>
  );
}

export default App;
