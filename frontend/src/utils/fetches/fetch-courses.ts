import { authenticatedFetch } from "../authenticated-fetch.ts";
const API_URL = import.meta.env.VITE_APP_API_HOST;

export const fetchCourses = async (user_uid: string) => {
  try {
    const response = await authenticatedFetch(
      `${API_URL}/courses?teacher=${user_uid}`,
    );
    const jsonData = await response.json();
    if (jsonData.data) {
      return jsonData.data;
    } else {
      return [];
    }
  } catch (_) {
    return [];
  }
};
