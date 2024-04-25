import { NavigateFunction, Params } from "react-router-dom";
import { authenticatedFetch } from "../../utils/authenticated-fetch";

export interface Course {
  course_id: string;
  name: string;
  teacher: string;
  ufora_id: string;
  url: string;
}

export interface Project {
  title: string;
  project_id: string;
  deadlines: string[][];
}

export const apiHost = import.meta.env.VITE_APP_API_HOST;
export const appHost = import.meta.env.VITE_APP_HOST;
/**
 * @returns The uid of the acces token of the logged in user
 */
export function loggedInToken() {
  return "teacher1";
}

/**
 * Get the username based on the provided uid.
 * @param uid - The uid of the user.
 * @returns The username.
 */
export function getUserName(uid: string): string {
  return getIdFromLink(uid);
}

/**
 * @returns The Uid of the logged in user
 */
export function loggedInUid() {
  return "Gunnar";
}

/**
 * On a succesfull post the function will redirect to the data.url of the response, this should point to the detail page
 * @param data - course data to send to the api
 * @param navigate - function that allows the app to redirect
 */
export function callToApiToCreateCourse(
  data: string,
  navigate: NavigateFunction
) {
  authenticatedFetch(`${apiHost}/courses`, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: data,
  })
    .then((response) => response.json())
    .then((data) => {
      //But first also make sure that teacher is in the course admins list
      authenticatedFetch(`${apiHost}/courses/${getIdFromLink(data.url)}/admins`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ admin_uid: loggedInUid() }),
      });
      navigate(getIdFromLink(data.url)); // navigate to data.url
    });
}

/**
 * @param link - the link to the api endpoint
 * @returns the Id at the end of the link
 */
export function getIdFromLink(link: string): string {
  const parts = link.split("/");
  return parts[parts.length - 1];
}

/**
 * Function to find the nearest future date from a list of dates
 * @param dates - Array of dates
 * @returns The nearest future date
 */
export function getNearestFutureDate(dates: string[][]): Date | null {
  const now = new Date();
  const futureDates = dates
    .map((date) => new Date(date[1]))
    .filter((date) => date > now);
  if (futureDates.length === 0) return null;
  return futureDates.reduce((nearest, current) =>
    current < nearest ? current : nearest
  );
}

/**
 * Load courses for courses teacher page, this filters courses on logged in teacher uid
 * @returns A Promise that resolves to the loaded courses data.
 */

const fetchData = async (url: string, params?: URLSearchParams) => {
  let uri = `${apiHost}/${url}`;
  if (params) {
    uri += `?${params}`;
  }
  const res = await authenticatedFetch(uri);
  if (res.status !== 200) {
    throw new Response("Failed to fetch data", { status: res.status });
  }
  const jsonResult = await res.json();

  return jsonResult.data;
};

export const dataLoaderCourses = async () => {
  //const params = new URLSearchParams({ 'teacher': loggedInUid() });
  return fetchData(`courses`);
};

const dataLoaderCourse = async (courseId: string) => {
  return fetchData(`courses/${courseId}`);
};

const dataLoaderProjects = async (courseId: string) => {
  const params = new URLSearchParams({ course_id: courseId });
  return fetchData(`projects`, params);
};

const dataLoaderAdmins = async (courseId: string) => {
  return fetchData(`courses/${courseId}/admins`);
};

const dataLoaderStudents = async (courseId: string) => {
  return fetchData(`courses/${courseId}/students`);
};

export const dataLoaderCourseDetail = async ({
  params,
}: {
  params: Params;
}) => {
  const { courseId } = params;
  if (!courseId) {
    throw new Error("Course ID is undefined.");
  }
  const course = await dataLoaderCourse(courseId);
  const projects = await dataLoaderProjects(courseId);
  const admins = await dataLoaderAdmins(courseId);
  const students = await dataLoaderStudents(courseId);

  return { course, projects, admins, students };
};
