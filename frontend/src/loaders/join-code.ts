import { redirect } from "react-router-dom";
import i18next from "i18next";
import { authenticatedFetch } from "../utils/authenticated-fetch";

const API_URL = import.meta.env.VITE_APP_API_HOST;

/**
 * This function sends a request to the server to join a course with a given join code.
 * @returns - Redirects to the course page if the join code is valid
 */
export async function synchronizeJoinCode() {
  const queryParams = new URLSearchParams(window.location.search);
  const joinCode = queryParams.get("code");

  if (joinCode) {
    const response = await authenticatedFetch(
      `${API_URL}/courses/join`,{
        method: "POST",
        body: JSON.stringify({ join_code: joinCode }),
        headers: { "Content-Type": "application/json" },
      }
    );

    if (response.ok || response.status === 409) {
      const responseData = await response.json();
      return redirect(
        `/${i18next.language}/courses/${responseData.data.course_id}`
      );
    } else {
      throw new Error("Invalid join code");
    }
  } else {
    throw new Error("No join code provided");
  }
}
