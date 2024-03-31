// https://stackoverflow.com/questions/71769484/react-router-v6-nested-routes-with-i18n
import { useEffect } from "react";
import { Outlet, useParams, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

const SUPPORTED_LANGUAGES = ["en", "nl"];

/**
 *
 * @returns - An outlet that detects the language and assigns it to i18next directly.
 */
export default function LanguagePath() {
  const { i18n } = useTranslation();
  const { lang } = useParams();
  const navigate = useNavigate();
  const curPath = location.pathname;
  useEffect(() => {
    if (lang && i18n.resolvedLanguage !== lang) {
      if (SUPPORTED_LANGUAGES.includes(lang)) {
        i18n.changeLanguage(lang);
      } else {
        navigate("/" + i18n.resolvedLanguage + curPath, { replace: true });
      }
    }
  }, [lang, curPath, i18n, navigate]);
  return <Outlet />;
}
