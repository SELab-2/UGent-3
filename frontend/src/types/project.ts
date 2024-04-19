export interface Project {
  title: string;
  description: string;
  assignment_file: string;
  deadline: string;
  course_id: string;
  visible_for_students: boolean;
  archived: boolean;
  test_path: string;
  script_name: string;
  regex_expressions: [string];
}