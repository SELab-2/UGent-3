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

        return project_dict

    def delete(self, **kwargs):
        # TODO
        # id = request.args
        remove_id = kwargs['project_id']

        submissions = Submissions.query.all()
        print(submissions)

        deleted_project = Projects.query.filter_by(project_id=remove_id).first()
        # deleted_project = {}
        print(deleted_project)
        db.session.delete(deleted_project)
        db.session.commit()

        return {}, 200


project_detail_bp.add_url_rule('/projects/<int:project_id>', view_func=ProjectDetail.as_view('project_detail'))
