import { BrowserRouter } from "react-router-dom";
import { Header } from "./components/Header/Header";

/**
 * This component is the main application component that will be rendered by the ReactDOM. 
 * @returns - The main application component
 */
function App(): JSX.Element {
  return (
    <BrowserRouter>
      <Header />
    </BrowserRouter>
  );
}
export default App;