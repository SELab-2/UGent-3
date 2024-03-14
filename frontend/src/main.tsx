/**import React from 'react'
import ReactDOM from 'react-dom/client'
import './stylesheet.css'

import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import Root from "./routes/root"
import ErrorPage from './error-pages/error-page';
import Login_page from './routes/login';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
  children: [
    {
      path: "login",
      element: <Login_page/>
    }
  ]
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)**/

import ReactDOM from "react-dom";

import {
  Box,
  Button,
  Container,
  Typography
} from "@mui/material";

import { MsalProvider, useMsal} from "@azure/msal-react";
import { Configuration,  PublicClientApplication } from "@azure/msal-browser";

// MSAL configuration
const configuration: Configuration = {
    auth: {
        clientId: "41f7c599-fe36-4d1b-9aae-8fdda0dadecb",
        authority: 'https://login.microsoftonline.com/d7811cde-ecef-496c-8f91-a1786241b99c/',
        redirectUri: 'http://localhost:5173'
    }
};

const pca = await PublicClientApplication.createPublicClientApplication(configuration);

// Component
const AppProvider = () => (
    <MsalProvider instance={pca}>
        <div>
        <Container>
            <div>
                <Typography variant="h1" display="flex" justifyContent="center">Pigeonhole</Typography>
            </div>
            <div>
                <Typography variant= "h2" display="flex" justifyContent="center">Please log in to continue</Typography>
            </div>
            <div>
                <Box textAlign="center">
                <Button variant="contained" size="large"
                onClick={async () => {
                  try {
                    pca.loginRedirect({scopes:[]});
                } catch (err) {
                    // handle error
                }
                }}>
                Log in!</Button>
                </Box> 
            </div>
        </Container>
        </div>
    </MsalProvider>
);

ReactDOM.render(<AppProvider />, document.getElementById("root"));