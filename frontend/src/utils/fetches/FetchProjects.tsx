import { fetchMe } from "./FetchMe.ts";
import {Project, ProjectDeadline, ShortSubmission} from "../../pages/project/projectDeadline/ProjectDeadline.tsx";
const API_URL = import.meta.env.VITE_APP_API_HOST

export const fetchProjectPage = async () => {
  const projects = await fetchProjects()
  const me = await fetchMe()
  return {projects, me}
}

export const fetchProjects = async () => {

  try{
    const response = await fetch(`${API_URL}/projects`, {
      credentials: 'include'

    })
    const jsonData = await response.json();
    let formattedData: ProjectDeadline[] = await Promise.all( jsonData.data.map(async (item:Project) => {
      try{
        const url_split = item.project_id.split('/')
        const project_id = url_split[url_split.length -1]
        const response_submissions =  await (await fetch(encodeURI(`${API_URL}/submissions?project_id=${project_id}`), {
          credentials: 'include'

        })).json()

        //get the latest submission
        const latest_submission = response_submissions.data.map((submission:ShortSubmission) => ({
          submission_id: submission.submission_id,//this is the path
          submission_time: new Date(submission.submission_time),
          submission_status: submission.submission_status,
          grading: submission.grading
        }
        )).sort((a:ShortSubmission, b:ShortSubmission) => b.submission_time.getTime() - a.submission_time.getTime())[0];
        // fetch the course id of the project
        const project_item = await (await fetch(encodeURI(`${API_URL}/projects/${project_id}`), {  credentials: 'include'
        })).json()

        //fetch the course
        const response_courses = await (await fetch(encodeURI(`${API_URL}/courses/${project_item.data.course_id}`), {
          credentials: 'include'
        })).json()
        const course = {
          course_id: response_courses.data.course_id,
          name: response_courses.data.name,
          teacher: response_courses.data.teacher,
          ufora_id: response_courses.data.ufora_id
        }
        if(project_item.data.deadlines){
          return project_item.data.deadlines.map((d:string[]) => {
            return  {
              project_id: project_id,
              title: project_item.data.title,
              description: project_item.data.description,
              assignment_file: project_item.data.assignment_file,
              deadline: new Date(d[1]),
              deadline_description: d[0],
              course_id: Number(project_item.data.course_id),
              visible_for_students: Boolean(project_item.data.visible_for_students),
              archived: Boolean(project_item.data.archived),
              test_path: project_item.data.test_path,
              script_name: project_item.data.script_name,
              regex_expressions: project_item.data.regex_expressions,
              short_submission: latest_submission,
              course: course
            }
          })
        }
        // contains no dealine:
        return [{
          project_id: project_id,
          title: project_item.data.title,
          description: project_item.data.description,
          assignment_file: project_item.data.assignment_file,
          deadline: undefined,
          deadline_description: undefined,
          course_id: Number(project_item.data.course_id),
          visible_for_students: Boolean(project_item.data.visible_for_students),
          archived: Boolean(project_item.data.archived),
          test_path: project_item.data.test_path,
          script_name: project_item.data.script_name,
          regex_expressions: project_item.data.regex_expressions,
          short_submission: latest_submission,
          course: course
        }]

      }catch (e){
        return []
      }
    }

    ));
    formattedData = formattedData.flat()
    return formattedData
  } catch (e) {
    return []
  }
}
