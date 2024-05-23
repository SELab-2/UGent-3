import {authenticatedFetch} from "../authenticated-fetch.ts";

const API_URL = import.meta.env.VITE_APP_API_HOST;

export const fetchMe = async () => {
  try {
    const response = await authenticatedFetch(`${API_URL}/me`, {
      credentials: "include",
    });
    if (response.status == 200) {
      const data = await response.json();
      data.data.loggedIn = true
      return data.data;
    } else {
      return {loggedIn: false };
    }
  } catch (e) {
    return { loggedIn: false };
  }
};
