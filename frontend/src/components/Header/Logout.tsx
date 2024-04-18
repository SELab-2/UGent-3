import {Button} from "@mui/material";
import {Link} from 'react-router-dom';

const API_HOST = import.meta.env.VITE_APP_API_HOST;

/**
 * The Logout component for the application that will redirect to the correct logout link.
 * @returns - A Logout button
 */
export function LogoutButton(): JSX.Element {
  const link = `${API_HOST}/logout`;

  return <Button variant="contained" component={Link} to={link}>Log out</Button>
}