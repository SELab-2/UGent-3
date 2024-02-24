"""Submission API endpoint"""

from flask import Blueprint
from flask_restful import Resource
from project.models.submissions import Submissions as m_submissions

submissions_bp = Blueprint("submissions", __name__)

class Submissions(Resource):
    """API endpoint for the submissions"""

    def get(self, uid: str, pid: int) -> dict[str, any]:
        """Get all the submissions from a user for a project

        Args:
            uid (int): User ID
            pid (int): Project ID

        Returns:
            dict[str, int]: The list of submission URLs
        """

        a = m_submissions.query.filter_by(uid=uid, project_id=pid).count()

        return {"uid": uid, "pid": pid, "test": a}

    def post(self, uid: int, pid: int) -> dict[str, int]:
        """Post a new submission to a project

        Args:
            uid (int): User ID
            pid (int): Project ID

        Returns:
            dict[str, int]: The URL to the submission
        """
        return {"uid": uid, "pid": pid}

submissions_bp.add_url_rule(
    "/submissions/<string:uid>/<int:pid>",
    view_func=Submissions.as_view("submissions"))

class Submission(Resource):
    """API endpoint for the submission"""

    def get(self, uid: int, pid: int, sid: int) -> dict[str, int]:
        """Get the submission given an submission ID

        Args:
            uid (int): User ID
            pid (int): Project ID
            sid (int): Submission ID

        Returns:
            dict[str, int]: The submission
        """
        return {"uid": uid, "pid": pid, "sid": sid}

    def delete(self, uid: int, pid: int, sid: int) -> dict[str, int]:
        """Delete a submission given an submission ID

        Args:
            uid (int): User ID
            pid (int): Project ID
            sid (int): Submission ID

        Returns:
            dict[str, int]: Empty
        """
        return {"uid": uid, "pid": pid, "sid": sid}

submissions_bp.add_url_rule(
    "/submissions/<int:uid>/<int:pid>/<int:sid>",
    view_func=Submission.as_view("submission"))
