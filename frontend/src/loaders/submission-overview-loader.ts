import { Params } from "react-router-dom";
import { Me } from "../types/me";
import { Submission } from "../types/submission";
import { authenticatedFetch } from "../utils/authenticated-fetch";

const APIURL = import.meta.env.VITE_APP_API_HOST;

const fetchDisplaynameByUid = async (uids: [string]) => {
  const uidParams = new URLSearchParams();
  for (const uid of uids) {
    uidParams.append("uid", uid);
  }
  const uidUrl = `${APIURL}/users?` + uidParams;
  const response = await authenticatedFetch(uidUrl);
  const jsonData = await response.json();

  return jsonData.data;
};

/**
 * 
 * @param param0 - projectId
 * @returns - projectData and submissionsWithUsers
 */
export default async function loadSubmissionOverview({
  params,
}: {
  params: Params<string>;
}) {

  const projectId = params.projectId;
  const projectResponse = await authenticatedFetch(
    `${APIURL}/projects/${projectId}`
  );

  if (!projectResponse.ok) {
    if (projectResponse.status == 403) {
      throw new Response("Not authenticated", {status: 403});
    } else if (projectResponse.status == 404) {
      throw new Response("Not found", {status: 404});
    }
  }

  const projectData = (await projectResponse.json())["data"];

  const overviewResponse = await authenticatedFetch(
    `${APIURL}/projects/${projectId}/latest-per-user`
  );
  const jsonData = await overviewResponse.json();
  const uids = jsonData.data.map((submission: Submission) => submission.uid);
  const users = await fetchDisplaynameByUid(uids);

  const submissionsWithUsers = jsonData.data.map((submission: Submission) => {
    // Find the corresponding user for this submission's UID
    const user = users.find((user: Me) => user.uid === submission.uid);
    // Add user information to the submission
    return {
      ...submission,
      display_name: user.display_name,
    };
  });

  return {
    projectData,
    submissionsWithUsers,
  };
}
