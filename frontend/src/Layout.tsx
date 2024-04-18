import { Outlet } from "react-router-dom";
import { Header } from "./components/Header/Header.tsx";

/**
 * Basic layout component that will be used on all routes.
 * @returns The Layout component
 */
export function Layout(): JSX.Element {
  return (
    <>
      <Header />
      <Outlet />
    </>
  );
}