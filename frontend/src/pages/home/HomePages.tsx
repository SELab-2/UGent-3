import HomeStudent from './HomeStudent';
import Home from "./Home.tsx";
import Cookies from 'js-cookie';

/**
 * Gives the requested home page based on the login status
 * @returns - The home page component 
 */
export default function HomePages() {
  const loginStatus = Cookies.get('login_status');

  if (loginStatus === 'STUDENT') {
    return <HomeStudent />;
  } /*else if (loginStatus === 'TEACHER') {
    return <HomeTeacher />;
  }*/ else {
    return <Home />;
  }
}
