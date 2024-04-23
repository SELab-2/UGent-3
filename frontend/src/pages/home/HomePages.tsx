import HomePage from './HomePage.tsx';
import Home from "./Home.tsx";
import {useLoaderData} from "react-router-dom";
import {ProjectDeadline} from "../project/projectDeadline/ProjectDeadline.tsx";
import {Me} from "../../types/me.ts"

/**
 * Gives the requested home page based on the login status
 * @returns - The home page component 
 */
export default function HomePages() {
  const loader = useLoaderData() as {
    projects: ProjectDeadline[];
    me: Me;
  };
  const me = loader.me.role;
  if (me === "UNKNOWN") {
    return <Home />;
  } else {
    return <HomePage />;
  }
}
