from flask import Blueprint
from flask_restful import Resource, Api

projects_bp = Blueprint('projects', __name__)

class Projects(Resource):
    def get(self):
        return {'hello': 'world'}


projects_bp.add_url_rule('/projects/', view_func=Projects.as_view('projects'))
