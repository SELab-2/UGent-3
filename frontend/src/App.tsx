import { RouterProvider, createBrowserRouter } from "react-router-dom";
import Home from "./pages/home/Home.tsx";
import { Layout } from "./Layout.tsx";
import { ErrorBoundary } from "./pages/error/ErrorBoundary.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    Component: Layout ,
    errorElement: <ErrorBoundary />,
    children: [
      {
        index: true,
        Component: Home
      }
    ]
  }
]);

/**
 * This component is the main application component that will be rendered by the ReactDOM. 
 * @returns The main application component
 */
export default function App(): React.JSX.Element {
  return <RouterProvider router={router} />;
}
