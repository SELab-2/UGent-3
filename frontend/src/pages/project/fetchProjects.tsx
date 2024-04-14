import React from "react";
import {Project, ProjectDeadline, ShortSubmission} from "./projectDeadline/ProjectDeadline.tsx";

export const fetchProjects = async (setProjects: React.Dispatch<React.SetStateAction<ProjectDeadline[]>>) => {
  const apiUrl = import.meta.env.VITE_APP_API_URL

  const header  = {
    "Authorization": "teacher2"
  }
  const response = await fetch(`${apiUrl}/projects`, {
    headers:header
  })
  const jsonData = await response.json();
  let formattedData: ProjectDeadline[] = await Promise.all( jsonData.data.map(async (item:Project) => {
    const project_id = item.project_id.split('/')[1]
    const response_submissions = await (await fetch(encodeURI(`${apiUrl}/submissions?&project_id=${project_id}`), {
      headers: header
    })).json()

    //get the latest submission
    const latest_submission = response_submissions.data.map((submission:ShortSubmission) => ({
      submission_id: submission.submission_id,//this is the path 
      submission_time: new Date(submission.submission_time),
      submission_status: submission.submission_status,
      grading: Number(submission.grading)
    }
    )).sort((a:ShortSubmission, b:ShortSubmission) => b.submission_time.getTime() - a.submission_time.getTime())[0];
    // fetch the course id of the project
    const project_item = await (await fetch(encodeURI(`${apiUrl}/${item.project_id}`), {
      headers:header
    })).json()

    //fetch the course
    const response_courses = await (await fetch(encodeURI(`${apiUrl}/courses/${project_item.data.course_id}`), {
      headers: header
    })).json()
    const course = {
      course_id: response_courses.data.course_id,
      name: response_courses.data.name,
      teacher: response_courses.data.teacher,
      ufora_id: response_courses.data.ufora_id
    }
    return item.deadlines.map((d:string[]) => {
      return  {
        project_id: item.project_id,
        title: item.title,
        description: item.description,
        assignment_file: item.assignment_file,
        deadline: new Date(d[1]),
        deadline_description: d[0],
        course_id: Number(item.course_id),
        visible_for_students: Boolean(item.visible_for_students),
        archived: Boolean(item.archived),
        test_path: item.test_path,
        script_name: item.script_name,
        regex_expressions: item.regex_expressions,
        short_submission: latest_submission,
        course: course
      }
    })
  }));
  formattedData = formattedData.flat()
  setProjects(formattedData);
  return formattedData
}