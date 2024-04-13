export interface ProjectDeadline {
  project_id:string ,
  title :string,
  description:string,
  assignment_file:string,
  deadline:Deadline,
  course_id:number,
  visible_for_students:boolean,
  archived:boolean,
  test_path:string,
  script_name:string,
  regex_expressions:string[],
  short_submission: ShortSubmission,
  course:Course

}
export interface Deadline {
  description: string;
  deadline: Date;
}

export interface Course {
  course_id: string;
  name: string;
  teacher: string;
  ufora_id: string;
}
export interface ShortSubmission {
  submission_id:number,
  submission_time:Date,
  submission_status:string
}


