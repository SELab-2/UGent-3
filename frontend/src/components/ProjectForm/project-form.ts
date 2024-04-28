import { fetchMe } from "../../utils/fetches/FetchMe.ts";
import {fetchProjectFormCourses} from "../Courses/courses.ts";

/**
 * Fetches the courses of the current user
 * @returns Course[]
 */
export async function fetchProjectForm (){
  const me = await fetchMe();
  return await fetchProjectFormCourses(me.uid);
}