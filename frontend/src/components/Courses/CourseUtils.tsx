import { NavigateFunction, Params } from "react-router-dom";
import { authenticatedFetch } from "../../utils/authenticated-fetch";
import { Me } from "../../types/me";
import { fetchMe } from "../../utils/fetches/FetchMe";

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
}

export interface ProjectDetail {
  title: string;
  project_id: string;
  deadlines: Deadline[];
}

interface Deadline {
  description: string;
  date: Date;
}

export const apiHost = import.meta.env.VITE_APP_API_HOST;
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
export async function getUser(uid: string): Promise<Me> {
  return authenticatedFetch(`${apiHost}/users/${getIdFromLink(uid)}`).then(
    (response) => {
      if (response.ok) {
        return response.json().then((data) => {
          return data.data;
        });
      }
    }
  );
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
 * Function to find the nearest future deadline from a list of deadlines
 * @param deadlines - List of deadlines
 * @returns The nearest future deadline
 */
export function getNearestFutureDate(deadlines: Deadline[]): Deadline | null {
  const now = new Date();
  const futureDeadlines = deadlines.filter((deadline) => deadline.date > now);
  if (futureDeadlines.length === 0) return null;
  return futureDeadlines.reduce((nearest, current) =>
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

  const courses = await fetchData(`courses`);
  const projects = await fetchProjectsCourse(courses);
  const me = await fetchMe();
  for (const c of courses) {
    const teacher = await fetchData(`users/${c.teacher}`);
    c.teacher = teacher.display_name;
  }
  return { courses, projects, me };
};

/**
 * Fetch the projects for the Course component
 * @param courses - All the courses
 * @returns the projects
 */
export async function fetchProjectsCourse(courses: Course[]) {
  const projectPromises = courses.map((course) =>
    authenticatedFetch(
      `${apiHost}/projects?course_id=${getIdFromLink(course.course_id)}`
    ).then((response) => response.json())
  );

  const projectResults = await Promise.all(projectPromises);
  const projectsMap: { [courseId: string]: ProjectDetail[] } = {};
  for await (const [index, result] of projectResults.entries()) {
    projectsMap[getIdFromLink(courses[index].course_id)] = await Promise.all(
      result.data.map(async (item: Project) => {
        const projectRes = await authenticatedFetch(item.project_id);
        if (projectRes.status !== 200) {
          throw new Response("Failed to fetch project data", {
            status: projectRes.status,
          });
        }
        const projectJson = await projectRes.json();
        const projectData = projectJson.data;
        let projectDeadlines = [];
        if (projectData.deadlines) {
          projectDeadlines = projectData.deadlines.map(
            ([description, dateString]: [string, string]) => ({
              description,
              date: new Date(dateString),
            })
          );
        }
        const project: ProjectDetail = {
          ...item,
          deadlines: projectDeadlines,
        };
        return project;
      })
    );
  }
  return { ...projectsMap };
}

const dataLoaderCourse = async (courseId: string) => {
  return fetchData(`courses/${courseId}`);
};

const dataLoaderProjects = async (courseId: string) => {
  const params = new URLSearchParams({ course_id: courseId });
  const uri = `${apiHost}/projects?${params}`;

  const res = await authenticatedFetch(uri);
  if (res.status !== 200) {
    throw new Response("Failed to fetch data", { status: res.status });
  }
  const jsonResult = await res.json();
  const projects: ProjectDetail[] = jsonResult.data.map(
    async (item: Project) => {
      const projectRes = await authenticatedFetch(item.project_id);
      if (projectRes.status !== 200) {
        throw new Response("Failed to fetch project data", {
          status: projectRes.status,
        });
      }
      const projectJson = await projectRes.json();
      const projectData = projectJson.data;
      let projectDeadlines = [];
      if (projectData.deadlines) {
        projectDeadlines = projectData.deadlines.map((deadline: Deadline) => ({
          description: deadline.description,
          date: new Date(deadline.date),
        }));
      }
      const project: ProjectDetail = {
        ...item,
        deadlines: projectDeadlines,
      };
      return project;
    }
  );

  return Promise.all(projects);
};

const dataLoaderAdmins = async (courseId: string) => {
  return fetchData(`courses/${courseId}/admins`);
};

const dataLoaderStudents = async (courseId: string) => {
  return fetchData(`courses/${courseId}/students`);
};

const fetchMes = async (uids: string[]) => {
  return Promise.all(uids.map((uid) => getUser(uid)));
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
  const me = await fetchMe();

  const course = await dataLoaderCourse(courseId);

  const courseAdminuids = course["admins"].map((admin: string) => {
    const urlSplit = admin.split("/");
    return urlSplit[urlSplit.length - 1];
  });

  const projects = await dataLoaderProjects(courseId);
  let adminMes: Me[] = [];
  if (me.uid === course.teacher || courseAdminuids.includes(me.uid)) {
    const admins = await dataLoaderAdmins(courseId);
    const adminUids = admins.map((admin: { uid: string }) =>
      getIdFromLink(admin.uid)
    );
    adminMes = await fetchMes([course.teacher, ...adminUids]);
  }
  const students = await dataLoaderStudents(courseId);
  const student_uids = students.map((student: { uid: string }) =>
    getIdFromLink(student.uid)
  );
  const studentMes = await fetchMes(student_uids);
  return { course, projects, adminMes, studentMes, me };
};
