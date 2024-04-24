export const fetchMe = async () => {
  const API_URL = import.meta.env.VITE_APP_API_HOST;
  try {
    const response = await fetch(`${API_URL}/me`, {
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
