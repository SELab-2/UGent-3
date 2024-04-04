import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

<<<<<<< HEAD
=======
const detectionOptions = {
  order: ['path', 'navigator', 'localStorage', 'subdomain', 'queryString', 'htmlTag'],
  lookupFromPathIndex: 0
}

>>>>>>> 496cd4d46088996ae3cfaf370e5edde8b6eff8b9
i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    debug: true,
<<<<<<< HEAD

=======
    detection: detectionOptions,
>>>>>>> 496cd4d46088996ae3cfaf370e5edde8b6eff8b9
    interpolation: {
      escapeValue: false,
    }
  });

export default i18n;
