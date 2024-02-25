from flask import Blueprint, request
from flask_restful import Resource, Api, abort, reqparse

from project import db
from project.models.projects import Projects
from project.models.submissions import Submissions

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

    def is_existing_project(self, project):
        if project is None:
            abort(404)

    def get(self, **kwargs):
        """
        Get method for listing a specific project
        filtered by id of that specific project
        """
        id: int = kwargs['project_id']

        project = Projects.query.filter_by(project_id=id).first()

        self.is_existing_project(project)

        project_dict = {field: value for field, value in project.__dict__.items() if
                        not field.startswith('_')}

        return project_dict, 200

    def put(self, **kwargs):
        id: int = kwargs['project_id']

        args = parser.parse_args()
        print(args)

        values = {key: value for key, value in args.items() if value is not None}

        project = Projects.query.filter_by(project_id=id).first()  # .update(values=values)

        for key, value in args.items():
            if value is not None:
                setattr(project, key, value)

        db.session.commit()
        return {"Message": f"Project {id} updated succesfully"}, 200

    def delete(self, **kwargs):
        """
        Detele a project and all of its submissions in cascade
        done by project id
        """

        remove_id = kwargs['project_id']

        deleted_project = Projects.query.filter_by(project_id=remove_id).first()

        self.is_existing_project(deleted_project)

        db.session.delete(deleted_project)
        db.session.commit()

        return {"Message": f"Project with id:{remove_id} deleted successfully!"}, 204


project_detail_bp.add_url_rule('/projects/<int:project_id>', view_func=ProjectDetail.as_view('project_detail'))
