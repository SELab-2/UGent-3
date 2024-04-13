import { useTranslation } from "react-i18next";
import { Title } from "../../components/Header/Title";
/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function Home() {
  const { t } = useTranslation("translation", { keyPrefix: "home" });
  return (
    <>
      <Title title={t('title')} />
      <div>
      </div>
    </>
  );
}
