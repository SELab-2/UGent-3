import {Outlet, useLoaderData} from "react-router-dom";
import { Header } from "./Header.tsx";
import {Me} from "../../types/me.ts"

/**
 * Basic layout component that will be used on all routes.
 * @returns The Layout component
 */
export default function Layout(): JSX.Element {
  const meData:Me = useLoaderData() as Me

  return (
    <>
      <Header me={meData} />
      <Outlet />
    </>
  );
}