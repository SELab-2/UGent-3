import { useRouteError, isRouteErrorResponse } from "react-router-dom";
import { ErrorPage } from "./ErrorPage.tsx";
import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { fetchMe } from "../../utils/fetches/FetchMe.ts";
import { Me } from "../../types/me.ts";
import { Header } from "../../components/Header/Header.tsx";

/**
 * This component will render the ErrorPage component with the appropriate data when an error occurs.
 * @returns The ErrorBoundary component
 */
export function ErrorBoundary() {
  const [me, setMe] = useState<Me | null>(null);

  useEffect(() => {
    fetchMe().then((data) => {
      setMe(data);
    });
  }, []);

  return (
    <>
      {me && <Header me={me} />}
      <ErrorBoundaryPage />
    </>
  );
}

const ErrorBoundaryPage = () => {
  const error = useRouteError();
  const { t } = useTranslation("translation", { keyPrefix: "error" });

  if (isRouteErrorResponse(error)) {
    if (error.status == 404) {
      return (
        <ErrorPage
          statusCode={"404"}
          statusTitle={t("pageNotFound")}
          message={t("pageNotFoundMessage")}
        />
      );
    } else if (error.status == 403) {
      return (
        <ErrorPage
          statusCode={"403"}
          statusTitle={t("forbidden")}
          message={t("forbiddenMessage")}
        />
      );
    } else if (error.status >= 400 && error.status <= 499) {
      return (
        <ErrorPage
          statusCode={error.statusText}
          statusTitle={t("clientError")}
          message={t("clientErrorMessage")}
        />
      );
    } else if (error.status >= 500 && error.status <= 599) {
      return (
        <ErrorPage
          statusCode={error.statusText}
          statusTitle={t("serverError")}
          message={t("serverErrorMessage")}
        />
      );
    } else {
      return (
          <ErrorPage
              statusCode={error.statusText}
              statusTitle={t("serverError")}
              message={t("serverErrorMessage")}
          />
      );
    }
  }
};
