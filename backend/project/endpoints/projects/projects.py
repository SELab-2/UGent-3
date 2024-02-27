"""
Module that implements the /projects endpoint of the API
"""

from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse

from project import db
from project.models.projects import Projects
from sqlalchemy import exc

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


class ProjectsEndpoint(Resource):
    """
    Class for projects endpoints
    Inherits from flask_restful.Resource class
    for implementing get method
    """
    def get(self):
        """
        Get method for listing all available projects
        that are currently in the API
        """
        display_data = []
        projects = Projects.query.all()

        # return all valid entries for a project and return a 200 OK code
        return jsonify(projects)

    def post(self):
        """
        Post functionality for project
        using flask_restfull parse lib
        """
        args = parser.parse_args()

        # create a new project object to add in the API later
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

        print(new_project)

        # add the new project to the database and commit the changes
        try:
            db.session.add(new_project)
            db.session.commit()
            return jsonify(new_project), 201
        except exc.SQLAlchemyError:
            return {"message": f"Something unexpected happenend when trying to add a new project"}, 500


projects_bp.add_url_rule('/projects', view_func=ProjectsEndpoint.as_view('projects'))
