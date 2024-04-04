import { useTranslation } from "react-i18next";

/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function Home() {
  const { t } = useTranslation();
  return (
    <div>
<<<<<<< HEAD
      <h1>{t('homepage')}</h1>
=======
      <h1></h1>
>>>>>>> 496cd4d46088996ae3cfaf370e5edde8b6eff8b9
    </div>
  );
}
