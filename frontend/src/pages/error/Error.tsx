import { isRouteErrorResponse, useRouteError } from "react-router-dom"

/**
 * This component is the error page component that will be rendered when an error occurs.
 * @returns - The error page component
 */
export function Error() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {

    let message = "";
    if (error.status == 403) {
      message = "Forbidden"
    } else if (error.status == 404) {
      message = "Page not found";
    } else if (error.status == 500) {
      message = "Internal server error";
    } else if (error.status == 503) {
      message = "Looks like our API is down";
    } else if (500 <= error.status && error.status <= 599) {
      message = "General server error";
    }

    return(
      <div>
        <h1>
          { error.status }
        </h1>
        <p>
          { message }
        </p>
      </div>
    )
  }
}