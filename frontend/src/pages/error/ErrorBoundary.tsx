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
        <ErrorPage statusCode={"404"} statusTitle={"Page Not Found"} message={"page_not_found_message"} />
      );
    }
    if (error.status == 403) {
      return (
        <ErrorPage statusCode={"403"} statusTitle={"Forbidden"} message={"forbidden_message"} />
      );
    }
    if (error.status >= 500 && error.status <= 599) {
      return (
        <ErrorPage statusCode={error.statusText} statusTitle={"Server Error"} message={"server_error_message"} />
      );
    }
  }
}
