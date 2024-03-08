import { Outlet } from "react-router-dom";

/**
 * @returns The root component.
 */
export default function Root() {
  return (
    <>
      {/* all the other elements */}
      <div id="detail">
        <Outlet />
      </div>
    </>
  );
}