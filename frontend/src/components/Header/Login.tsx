import {Button} from "@mui/material";
import { Link } from 'react-router-dom';
import {useTranslation} from "react-i18next";

const CLIENT_ID = import.meta.env.VITE_APP_CLIENT_ID;
const REDIRECT_URI = encodeURI(import.meta.env.VITE_APP_API_HOST + "/auth");
const TENANT_ID = import.meta.env.VITE_APP_TENANT_ID;

/**
 * The login component for the application that will redirect to the correct login link.
 * @returns - A login button
 */
export function LoginButton(): JSX.Element {
  const link = `https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/authorize?prompt=select_account&response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=.default`;
  const { t } = useTranslation('translation', { keyPrefix: 'home' });

  return <Button variant="contained" component={Link} to={link}> {t('login', 'Login')}</Button>
}
