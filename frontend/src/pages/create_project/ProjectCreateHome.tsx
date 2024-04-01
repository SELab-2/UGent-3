/**
 *
 */
import ProjectForm from "../../components/ProjectForm/ProjectForm.tsx";
import {Box} from "@mui/material";

/**
 *
 * @param root0
 * @param root0.setHeaderText
 */
export default function ProjectCreateHome({ setHeaderText }) {
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
