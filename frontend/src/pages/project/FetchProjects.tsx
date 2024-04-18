import {Project, ProjectDeadline, ShortSubmission} from "./projectDeadline/ProjectDeadline.tsx";
const API_URL = import.meta.env.VITE_APP_API_HOST
const header  = {
  "Authorization": "teacher2"
}
export const fetchProjectPage = async () => {
  const projects = await fetchProjects()
  const me = await fetchMe()
  return {projects, me}
}

export const fetchMe = async () => {
  try {
    const response = await fetch(`${API_URL}/me`, {
      headers:header
    })
    if(response.status == 200){
      const data  = await response.json()
      return data.role
    }else {
      return "UNKNOWN"
    }
  } catch (e){
    return "UNKNOWN"
  }

}
export const fetchProjects = async () => {

  try{
    const response = await fetch(`${API_URL}/projects`, {
      headers:header
    })
    const jsonData = await response.json();
    let formattedData: ProjectDeadline[] = await Promise.all( jsonData.data.map(async (item:Project) => {
      try{
        const url_split = item.project_id.split('/')
        const project_id = url_split[url_split.length -1]
        const response_submissions =  await (await fetch(encodeURI(`${API_URL}/submissions?project_id=${project_id}`), {
          headers: header
        })).json()

        //get the latest submission
        const latest_submission = response_submissions.data.map((submission:ShortSubmission) => ({
          submission_id: submission.submission_id,//this is the path
          submission_time: new Date(submission.submission_time),
          submission_status: submission.submission_status
        }
        )).sort((a:ShortSubmission, b:ShortSubmission) => b.submission_time.getTime() - a.submission_time.getTime())[0];
          // fetch the course id of the project
        const project_item = await (await fetch(encodeURI(`${API_URL}/projects/${project_id}`), {
          headers:header
        })).json()

        //fetch the course
        const response_courses = await (await fetch(encodeURI(`${API_URL}/courses/${project_item.data.course_id}`), {
          headers: header
        })).json()
        const course = {
          course_id: response_courses.data.course_id,
          name: response_courses.data.name,
          teacher: response_courses.data.teacher,
          ufora_id: response_courses.data.ufora_id
        }
        if(item.deadlines){
          return item.deadlines.map((d:string[]) => {
            return  {
              project_id: project_id,
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
        }
        // contains no dealine:
        return [{
          project_id: project_id,
          title: item.title,
          description: item.description,
          assignment_file: item.assignment_file,
          deadline: undefined,
          deadline_description: undefined,
          course_id: Number(item.course_id),
          visible_for_students: Boolean(item.visible_for_students),
          archived: Boolean(item.archived),
          test_path: item.test_path,
          script_name: item.script_name,
          regex_expressions: item.regex_expressions,
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
