export const fetchMe = async () => {
  const API_URL = import.meta.env.VITE_APP_API_HOST;
  try {
    const response = await fetch(`${API_URL}/me`, {
      credentials: "include",
    });
    if (response.status == 200) {
      const data = await response.json();
      return data.data;
    } else {
      return { role: "UNKNOWN" };
    }
  } catch (e) {
    return { role: "UNKNOWN" };
  }
};
