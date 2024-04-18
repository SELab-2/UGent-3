import {Button} from "@mui/material";
import { Link } from 'react-router-dom';

const CODE_VERIFIER = import.meta.env.VITE_APP_CODE_VERIFIER;
const CLIENT_ID = import.meta.env.VITE_APP_CLIENT_ID;
const REDIRECT_URI = encodeURI(import.meta.env.VITE_APP_API_HOST + "/auth");
const TENANT_ID = import.meta.env.VITE_APP_TENANT_ID;

/**
 * A function to hash a string using SHA256.
 * @returns - A hashed string
 */
async function hash(string: string) {
  
  const utf8 = new TextEncoder().encode(string);
  return crypto.subtle.digest('SHA-256', utf8).then((hashBuffer) => {
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((bytes) => bytes.toString(16).padStart(2, '0'))
      .join('');
    return hashHex;
  });
}

/**
 * The login component for the application that will redirect to the correct login link.
 * @returns - A login button
 */
export async function LoginLink(): Promise<JSX.Element> {
  
  const code_challenge = btoa(await hash(CODE_VERIFIER));
  const link = `https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/authorize?prompt=select_account&response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=.default&code_challenge=${code_challenge}&code_challenge_method=S256`;

  return <Button variant="contained" component={Link} to={link}>Login</Button>
}
