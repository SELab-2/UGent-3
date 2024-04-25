import { redirect } from "react-router-dom";
import i18next from "i18next";
import { getCSRFCookie } from "../utils/csrf";

const API_URL = import.meta.env.VITE_APP_API_HOST;


export async function synchronizeJoinCode() {
  const queryParams = new URLSearchParams(window.location.search);
  const joinCode = queryParams.get("code");

  if (joinCode) {
    const response = await fetch(new URL("/courses/join", API_URL), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": getCSRFCookie(),
      },
      credentials: "include",
      body: JSON.stringify({
        join_code: joinCode,
      }),
    });

    if (response.ok) {
      const responseData = await response.json();
      return redirect(
        `/${i18next.language}/courses/${responseData.data.course_id}`
      );
    }
  } else {
    throw new Error("No join code provided");
  }
}
