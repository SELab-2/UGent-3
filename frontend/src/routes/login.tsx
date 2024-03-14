import {
    Box,
    Button,
    Container,
    Typography
} from "@mui/material";

/**
 * This component is the login page component that will be rendered when on the index route and not yet logged in.
 * @returns - The login page component
 */
export default function Login_page() {
    return (
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
                onClick={() => {
                    
                }}>
                Log in!</Button>
                </Box> 
            </div>
        </Container>
        </div>
    );
  }