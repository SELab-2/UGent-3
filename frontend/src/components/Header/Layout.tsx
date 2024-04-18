import { Outlet } from "react-router-dom";
import { Header } from "./Header.tsx";

/**
 * Basic layout component that will be used on all routes.
 * @returns The Layout component
 */
export default function Layout(): JSX.Element {
  return (
    <>
      <Header />
      <Outlet />
    </>
  );
}