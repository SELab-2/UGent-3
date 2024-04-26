import { fetchMe } from "./FetchMe.ts";
import { fetchCourses } from "./fetch-courses.ts";

export const fetchProjectForm = async () => {
  const me = await fetchMe();
  return await fetchCourses(me.uid);
}; 