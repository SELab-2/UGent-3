/**
 *
 */
import ProjectForm from "../../components/ProjectForm/ProjectForm.tsx";
import {Box} from "@mui/material";

/**
 * Renders the home page for creating a project.
 * @returns ProjectCreateHome - Returns the JSX element representing the home page for creating a project.
 */
export default function ProjectCreateHome() {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
      }}
    >
      <ProjectForm />
    </Box>
  )
  ;
}
