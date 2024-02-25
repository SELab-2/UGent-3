from flask import Blueprint
from flask_restful import Resource, Api
from sqlalchemy.orm import sessionmaker

from project import db
from project.models.projects import Projects

projects_bp = Blueprint('projects', __name__)
projects_endpoint = Api(projects_bp)
class Projects_endpoint(Resource):
    def get(self):
        """
        Get method for listing all available projects
        that are currently in the API
        """
        # TODO: fetch data from database using sqlalchemy
        display_data = {}
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
            print(project_dict)

        return {'hello': 'world'}


projects_bp.add_url_rule('/projects/', view_func=Projects_endpoint.as_view('projects'))
