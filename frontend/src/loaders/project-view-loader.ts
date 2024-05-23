import { Params } from "react-router-dom";
import { Deadline } from "../types/deadline";
import { authenticatedFetch } from "../utils/authenticated-fetch";
import { fetchMe } from "../utils/fetches/FetchMe";
import i18next from "i18next";

const API_URL = import.meta.env.VITE_APP_API_HOST;

export default async function loadProjectViewData({
  params,
}: {
  params: Params<string>;
}) {
  const me = await fetchMe();

  const projectId = params.projectId;

  const assignmentResponse = await authenticatedFetch(
    `${API_URL}/projects/${projectId}/assignment?lang=${i18next.resolvedLanguage}`
  );

  let assignmentText;

  if (assignmentResponse.ok) {
    assignmentText = await assignmentResponse.text();
  } else {
    throw new Response(assignmentResponse.statusText, {
      status: assignmentResponse.status,
    });
  }

  const response = await authenticatedFetch(`${API_URL}/projects/${projectId}`);
  if (response.ok) {
    const data = await response.json();
    const projectData = data["data"];

    const transformedDeadlines = projectData.deadlines.map(
      (deadlineArray: string[]): Deadline => ({
        description: deadlineArray[0],
        deadline: deadlineArray[1],
      })
    );

    projectData["deadlines"] = transformedDeadlines;

    const courseResponse = await authenticatedFetch(
      `${API_URL}/courses/${projectData.course_id}`
    );

    let courseData;
    if (courseResponse.ok) {
      courseData = (await courseResponse.json())["data"];
    } else {
      throw new Response(response.statusText, { status: response.status });
    }

    courseData["admins"] = courseData["admins"].map((admin: string) => {
      const urlSplit = admin.split("/");
      return urlSplit[urlSplit.length - 1];
    });

    const isAdmin =
      me.uid === courseData["teacher"] || courseData["admins"].includes(me.uid);

    console.log(courseData);

    return {
      projectData: projectData,
      courseData: courseData,
      me: me,
      assignmentText: assignmentText,
      isAdmin: isAdmin,
    };
  } else {
    throw new Response(response.statusText, { status: response.status });
  }
}
