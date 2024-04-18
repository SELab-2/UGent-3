import {Link} from "@mui/material";

const CODE_VERIFIER = import.meta.env.VITE_APP_CODE_VERIFIER;
const CLIENT_ID = import.meta.env.VITE_APP_CLIENT_ID;
const REDIRECT_URI = encodeURI(import.meta.env.VITE_APP_API_HOST + "/auth");
const TENANT_ID = import.meta.env.VITE_APP_TENANT_ID;

export function LoginLink(): JSX.Element {
    const code_challenge = crypto.createHash('sha256')
        .update(CODE_VERIFIER)
        .digest('base64');
    const link = `https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/authorize?prompt=select_account&response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=.default&code_challenge=${code_challenge}&code_challenge_method=S256&state=?`;
    return (<Link href=`${link}`>Login</Link>)
};
