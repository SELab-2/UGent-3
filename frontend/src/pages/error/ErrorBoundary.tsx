import { useRouteError, isRouteErrorResponse } from "react-router-dom";
import { ErrorPage } from "./ErrorPage.tsx";

/**
 * This component will render the ErrorPage component with the appropriate data when an error occurs.
 * @returns The ErrorBoundary component
 */
export function ErrorBoundary() {
  const error = useRouteError();
  if (isRouteErrorResponse(error)) {
    if (error.status == 404) {
      return (
        <ErrorPage statusCode={"404"} statusTitle={"error.pageNotFound"} message={"error.pageNotFoundMessage"} />
      );
    } else if (error.status == 403) {
      return (
        <ErrorPage statusCode={"403"} statusTitle={"error.forbidden"} message={"error.forbiddenMessage"} />
      );
    } else if (error.status >= 400 && error.status <= 499) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={"error.clientError"} message={"error.clientErrorMessage"} />
      );
    } else if (error.status >= 500 && error.status <= 599) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={"error.serverError"} message={"error.serverErrorMessage"} />
      );
    }
  }
}
