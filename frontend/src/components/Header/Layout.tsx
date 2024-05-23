import {
  Outlet,
  useLoaderData,
  useLocation,
  useNavigate,
} from "react-router-dom";
import { Header } from "./Header.tsx";
import { Me } from "../../types/me.ts";
import { useEffect } from "react";
import i18next from "i18next";

/**
 * Basic layout component that will be used on all routes.
 * @returns The Layout component
 */
export default function Layout(): JSX.Element {
  const meData: Me = useLoaderData() as Me;
  useEnsureLangCodeInPath();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (
      !meData.loggedIn &&
      !(
        location.pathname === "/" ||
        /\/([a-z]{2})?\/home/.test(location.pathname)
      )
    ) {
      navigate("/");
    }
  }, [meData.loggedIn, location.pathname, navigate]);

  return (
    <>
      <Header me={meData} />
      <Outlet />
    </>
  );
}

const useEnsureLangCodeInPath = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const pathParts = location.pathname.split("/").filter(Boolean);
    const langCode = i18next.resolvedLanguage;

    // Check if the URL starts with the lang code
    if (pathParts[0] !== langCode) {
      // Prepend the lang code to the path
      const newPath = `/${langCode}/${pathParts.join("/")}`;
      navigate(newPath);
    }
  }, [location, navigate]);
};