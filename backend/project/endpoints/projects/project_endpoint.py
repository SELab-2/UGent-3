"""
Module for providing the blueprint to the api
of both routes
"""

from flask import Blueprint
from flask_restful import Api

from project.endpoints.projects.projects import ProjectsEndpoint
from project.endpoints.projects.project_detail import ProjectDetail

project_bp = Blueprint('project_endpoint', __name__)
project_endpoint = Api(project_bp)

project_bp.add_url_rule(
    '/projects',
    view_func=ProjectsEndpoint.as_view('project_endpoint')
)

project_bp.add_url_rule(
    '/projects/<int:project_id>',
    view_func=ProjectDetail.as_view('project_detail')
)
