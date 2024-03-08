import { useRouteError } from "react-router-dom";
/**
 * @returns the error page component.
 */
export default function ErrorPage() {
  const error = useRouteError() as Error;
  console.error(error);

  return (
    <div id="error-page">
      <h1>Oops!</h1>
      <p>Sorry, an unexpected error has occurred.</p>
      <p>
        <i>{error.message}</i>
      </p>
    </div>
  );
}