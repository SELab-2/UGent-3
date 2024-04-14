import { useRouteError, isRouteErrorResponse } from "react-router-dom";
import { ErrorPage } from "./ErrorPage.tsx";
import { useTranslation } from "react-i18next";

/**
 * This component will render the ErrorPage component with the appropriate data when an error occurs.
 * @returns The ErrorBoundary component
 */
export function ErrorBoundary() {
  const error = useRouteError();
  const { t } = useTranslation();

  if (isRouteErrorResponse(error)) {
    if (error.status == 404) {
      return (
        <ErrorPage statusCode={"404"} statusTitle={t("error.pageNotFound")} message={t("error.pageNotFoundMessage")} />
      );
    } else if (error.status == 403) {
      return (
        <ErrorPage statusCode={"403"} statusTitle={t("error.forbidden")} message={t("error.forbiddenMessage")} />
      );
    } else if (error.status >= 400 && error.status <= 499) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={t("error.clientError")} message={t("error.clientErrorMessage")} />
      );
    } else if (error.status >= 500 && error.status <= 599) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={t("error.serverError")} message={t("error.serverErrorMessage")} />
      );
    }
  }
}
