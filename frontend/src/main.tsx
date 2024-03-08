import React from 'react'
import ReactDOM from 'react-dom/client'
import './stylesheet.css'

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import Root from "./routes/root"
import ErrorPage from './error-pages/error-page';
import Login_page from './routes/login';
import {All_courses,Student_or_admin} from './routes/courses';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "login",
        element: <Login_page/>
      },
      {
        path: "courses",
        children: [
          {
            path: "",
            element: <All_courses />
          },
          {
            path: ":courseId",
            element: <Student_or_admin />
          }
        ]
      }
    ]
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)