from flask import Blueprint
from project.endpoints.submissions.submissions import SubmissionsEndpoint
from project.endpoints.submissions.submission_detail import SubmissionEndpoint
from project.endpoints.submissions.submission_download import SubmissionDownload

submissions_bp = Blueprint("submissions", __name__)


submissions_bp.add_url_rule("/submissions", view_func=SubmissionsEndpoint.as_view("submissions"))
submissions_bp.add_url_rule(
    "/submissions/<int:submission_id>",
    view_func=SubmissionEndpoint.as_view("submission")
)
submissions_bp.add_url_rule(
    "/submissions/<int:submission_id>/download",
    view_func=SubmissionDownload.as_view("submission_download")
)