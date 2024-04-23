import {Outlet, useLoaderData} from "react-router-dom";
import { Header } from "./Header.tsx";
import {me} from "../../types/me.ts"

/**
 * Basic layout component that will be used on all routes.
 * @returns The Layout component
 */
export default function Layout(): JSX.Element {
  const meData:me = useLoaderData() as me

  return (
    <>
      <Header me={meData} />
      <Outlet />
    </>
  );
}