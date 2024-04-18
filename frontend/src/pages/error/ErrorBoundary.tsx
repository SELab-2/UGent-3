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
  const keyPrefix = "error.";

  if (isRouteErrorResponse(error)) {
    if (error.status == 404) {
      return (
        <ErrorPage statusCode={"404"} statusTitle={t(keyPrefix + "pageNotFound")} message={t(keyPrefix + "pageNotFoundMessage")} />
      );
    } else if (error.status == 403) {
      return (
        <ErrorPage statusCode={"403"} statusTitle={t(keyPrefix + "forbidden")} message={t(keyPrefix + "forbiddenMessage")} />
      );
    } else if (error.status >= 400 && error.status <= 499) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={t(keyPrefix + "clientError")} message={t(keyPrefix + "clientErrorMessage")} />
      );
    } else if (error.status >= 500 && error.status <= 599) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={t(keyPrefix + "serverError")} message={t(keyPrefix + "serverErrorMessage")} />
      );
    }
  }
}
