import { useTranslation } from "react-i18next";

/**
 * This component is the home page component that will be rendered when on the index route.
 * @returns - The home page component
 */
export default function Home() {
  const { t } = useTranslation('translation', { keyPrefix: 'home' });
  return (
    <div>
      <h1>{t('homepage')}</h1>
    </div>
  );
}
