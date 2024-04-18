import { useRouteError, isRouteErrorResponse } from "react-router-dom";
import { ErrorPage } from "./ErrorPage.tsx";
import { useTranslation } from "react-i18next";

/**
 * This component will render the ErrorPage component with the appropriate data when an error occurs.
 * @returns The ErrorBoundary component
 */
export function ErrorBoundary() {
  const error = useRouteError();
  const { t } = useTranslation('translation', { keyPrefix: 'error' });

  if (isRouteErrorResponse(error)) {
    if (error.status == 404) {
      return (
        <ErrorPage statusCode={"404"} statusTitle={t("pageNotFound")} message={t("pageNotFoundMessage")} />
      );
    } else if (error.status == 403) {
      return (
        <ErrorPage statusCode={"403"} statusTitle={t("forbidden")} message={t("forbiddenMessage")} />
      );
    } else if (error.status >= 400 && error.status <= 499) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={t("clientError")} message={t("clientErrorMessage")} />
      );
    } else if (error.status >= 500 && error.status <= 599) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={t("serverError")} message={t("serverErrorMessage")} />
      );
    }
  }
}
