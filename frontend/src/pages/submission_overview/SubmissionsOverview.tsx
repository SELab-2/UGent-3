import {useTranslation} from "react-i18next";
import { Title } from "../../components/Header/Title.tsx";
import ProjectSubmissionOverview from "../../components/ProjectSubmissionOverview/ProjectSubmissionOverview.tsx";

/**
 *
 * @returns Wrapper for page of submissions overview
 */
export default function SubmissionsOverview() {

  const { t } = useTranslation('submissionOverview', { keyPrefix: 'submissionOverview' });

  return (<>
    <Title title={t("submissionOverviewHeader")}/>
    <ProjectSubmissionOverview/>
  </>)
}