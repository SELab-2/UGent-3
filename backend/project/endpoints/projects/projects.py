from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from sqlalchemy import insert, delete

from project import db
from project.models.projects import Projects
from project.models.courses import Courses

parser = reqparse.RequestParser()
# parser.add_argument('id', type=int, help='Unique to charge for this resource')
parser.add_argument('title', type=str, help='Projects title')
parser.add_argument('descriptions', type=str, help='Projects description')
parser.add_argument('assignment_file', type=str, help='Projects assignment file')
parser.add_argument("deadline", type=str, help='Projects deadline')
parser.add_argument("course_id", type=str, help='Projects course_id')
parser.add_argument("visible_for_students", type=bool, help='Projects visibility for students')
parser.add_argument("archieved", type=bool, help='Projects')
parser.add_argument("test_path", type=str, help='Projects test path')
parser.add_argument("script_name", type=str, help='Projects test script path')
parser.add_argument("regex_expressions", type=str, help='Projects regex expressions')

projects_bp = Blueprint('projects', __name__)
projects_endpoint = Api(projects_bp)
class Projects_endpoint(Resource):
    def get(self):
        """
        Get method for listing all available projects
        that are currently in the API
        """
        display_data = []
        projects = Projects.query.all()

        for project in projects:
            project_dict = {
                "id": project.project_id,
                "title": project.title,
                "descriptions": project.descriptions,
                "assignment_file": project.assignment_file,
                "deadline": project.deadline,
                "course_id": project.course_id,
                "visible_for_students": project.visible_for_students,
                "archieved": project.archieved,
                "test_path": project.test_path,
                "script_name": project.script_name,
                "regex_expressions": project.regex_expressions
            }
            display_data.append(project_dict)

        return display_data

    def post(self):
        """
        Post functionality for project
        using flask_restfull parse lib
        """
        args = parser.parse_args()
        print(args)

        new_project = Projects(
            title=args['title'],
            descriptions=args['descriptions'],
            assignment_file=args['assignment_file'],
            deadline=args['deadline'],
            course_id=args['course_id'],
            visible_for_students=args['visible_for_students'],
            archieved=args['archieved'],
            test_path=args['test_path'],
            script_name=args['script_name'],
            regex_expressions=args['regex_expressions']
        )

        db.session.add(new_project)
        db.session.commit()

        return args, 201


    def get_successor_id(self):
        pass

projects_bp.add_url_rule('/projects', view_func=Projects_endpoint.as_view('projects'))
