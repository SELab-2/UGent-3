/**
 *
 */
import ProjectForm from "../../components/ProjectForm/ProjectForm.tsx";
import {Box} from "@mui/material";

interface Props {
  setHeaderText?: (text: string) => void;
}

/**
 * Renders the home page for creating a project.
 * @param props - react props
 * @returns ProjectCreateHome - Returns the JSX element representing the home page for creating a project.
 */
export default function ProjectCreateHome({ setHeaderText }: Props) {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
      }}
    >
      <ProjectForm setHeaderText={setHeaderText}/>
    </Box>
  )
  ;
}
