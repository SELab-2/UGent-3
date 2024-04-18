import HomePage from './HomePage.tsx';
import Home from "./Home.tsx";
import {useLoaderData} from "react-router-dom";
import {ProjectDeadline} from "../project/projectDeadline/ProjectDeadline.tsx";

/**
 * Gives the requested home page based on the login status
 * @returns - The home page component 
 */
export default function HomePages() {
  const loader = useLoaderData() as {
    projects: ProjectDeadline[],
    me: string
  }
  const me = loader.me
  if (me === 'LOGGED_IN') {
    return <HomePage />;
  } else {
    return <Home />;
  }
}