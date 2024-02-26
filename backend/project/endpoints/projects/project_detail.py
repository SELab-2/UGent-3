"""
Module for project details page
for example /projects/1 if the project id of
the corresponding project is 1
"""

from flask import Blueprint, jsonify
from flask_restful import Resource, Api, abort, reqparse

from project import db
from project.models.projects import Projects

project_detail_bp = Blueprint('project_detail', __name__)
project_detail_endpoint = Api(project_detail_bp)

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


class ProjectDetail(Resource):
    """
    Class for projects/id endpoints
    Inherits from flask_restful.Resource class
    for implementing get, delete and put methods
    """

    def abort_if_not_present(self, project):
        """
        Check if the project exists in the database
        and if not abort the request and give back a 404 not found
        """
        if project is None:
            abort(404)

    def get(self, project_id):
        """
        Get method for listing a specific project
        filtered by id of that specific project
        the id fetched from the url with the reaparse
        """

        # fetch the project with the id that is specified in the url
        project = Projects.query.filter_by(project_id=project_id).first()

        self.abort_if_not_present(project)

        # return the fetched project and return 200 OK status
        return jsonify(project)

    def put(self, **kwargs):
        """
        Update method for updating a specific project
        filtered by id of that specific project
        """
        proj_id: int = kwargs['project_id']

        args = parser.parse_args()
        # get the project that need to be edited
        project = Projects.query.filter_by(project_id=proj_id).first()  # .update(values=values)

        # check which values are not None is the dict
        # if it is not None is needs to be modified in the database
        for key, value in args.items():
            if value is not None:
                setattr(project, key, value)

        # commit the changes and return the 200 OK code
        db.session.commit()
        return {"Message": f"Project {id} updated succesfully"}, 200

    def delete(self, **kwargs):
        """
        Detele a project and all of its submissions in cascade
        done by project id
        """

        remove_id = kwargs['project_id']

        # fetch the project that needs to be removed
        deleted_project = Projects.query.filter_by(project_id=remove_id).first()

        # check if its an existing one
        self.abort_if_not_present(deleted_project)

        # if it exists delete it and commit the changes in the database
        db.session.delete(deleted_project)
        db.session.commit()

        # return 204 content delted succesfully
        return {"Message": f"Project with id:{remove_id} deleted successfully!"}, 204


project_detail_bp.add_url_rule(
    '/projects/<int:project_id>',
    view_func=ProjectDetail.as_view('project_detail'))
