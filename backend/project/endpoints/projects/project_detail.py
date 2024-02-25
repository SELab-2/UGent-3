from flask import Blueprint, request
from flask_restful import Resource, Api

from project import db
from project.models.projects import Projects
from project.models.submissions import Submissions

project_detail_bp = Blueprint('project_detail', __name__)
project_detail_endpoint = Api(project_detail_bp)


class ProjectDetail(Resource):
    def get(self, **kwargs):
        """
        Get method for listing a specific project
        filtered by id of that specific project
        """
        id: int = kwargs['project_id']
        print(id)

        project = Projects.query.filter_by(project_id=id).first()

        if project is None:
            # project doesn't exist so return a 404 error
            return {'message': 'Project doesn\'t exist'}, 404

        print(project)
        project_dict = {field: value for field, value in project.__dict__.items() if
                            not field.startswith('_')}

        return project_dict, 200

    def delete(self, **kwargs):
        """
        Detele a project and all of its submissions in cascade
        done by project id
        """

        remove_id = kwargs['project_id']

        deleted_project = Projects.query.filter_by(project_id=remove_id).first()

        db.session.delete(deleted_project)
        db.session.commit()

        return {"Message": f"Project with id:{remove_id} deleted successfully!"}, 204


project_detail_bp.add_url_rule('/projects/<int:project_id>', view_func=ProjectDetail.as_view('project_detail'))
