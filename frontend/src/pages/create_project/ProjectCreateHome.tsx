/**
 *
 */
import { Title } from "../../components/Header/Title.tsx";
import ProjectForm from "../../components/ProjectForm/ProjectForm.tsx";
import {Box} from "@mui/material";
import {useTranslation} from "react-i18next";

/**
 * Renders the home page for creating a project.
 * @returns ProjectCreateHome - Returns the JSX element representing the home page for creating a project.
 */
export default function ProjectCreateHome() {

  const { t } = useTranslation('translation', { keyPrefix: 'projectForm' });

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
      }}
    >
      <Title title={t("projectHeader")}/>
      <ProjectForm/>
    </Box>
  )
  ;
}
