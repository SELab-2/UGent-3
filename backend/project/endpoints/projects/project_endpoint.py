"""
Module for providing the blueprint to the api
of both routes
"""

from flask import Blueprint

from project.endpoints.projects.projects import ProjectsEndpoint
from project.endpoints.projects.project_detail import ProjectDetail
from project.endpoints.projects.project_assignment_file import ProjectAssignmentFiles
from project.endpoints.projects.project_submissions_download import SubmissionDownload
from project.endpoints.projects.project_last_submission import SubmissionPerUser


project_bp = Blueprint('project_endpoint', __name__)

project_bp.add_url_rule(
    '/projects',
    view_func=ProjectsEndpoint.as_view('project_endpoint')
)

project_bp.add_url_rule(
    '/projects/<int:project_id>',
    view_func=ProjectDetail.as_view('project_detail')
)

project_bp.add_url_rule(
    '/projects/<int:project_id>/assignment',
    view_func=ProjectAssignmentFiles.as_view('project_assignment')
)

project_bp.add_url_rule(
    '/projects/<int:project_id>/submissions-download',
    view_func=SubmissionDownload.as_view('project_submissions')
)

project_bp.add_url_rule(
    '/projects/<int:project_id>/latest-per-user',
    view_func=SubmissionPerUser.as_view('latest_per_user')
)
