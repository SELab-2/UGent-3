"""Tests the submissions API endpoint"""

from typing import Tuple

from pytest import mark
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from tests.endpoints.endpoint import TestEndpoint, authentication_tests, authorization_tests
from project.models.user import User
from project.models.project import Project
from project.models.submission import Submission

class TestSubmissionsEndpoint(TestEndpoint):
    """Class to test the submissions API endpoint"""

    ### AUTHENTICATION & AUTHORIZATION ###
    # Where is login required
    # (endpoint, parameters, methods)
    authentication = authentication_tests([
        ("/submissions", [], ["get", "post"]),
        ("/submissions/@0", ["submission_id"], ["get", "patch", "delete"])
    ])

    # Who can access what
    # (endpoint, parameters, method, allowed, disallowed)
    authorization = authorization_tests([
        ("/submissions", [], "get",
            ["student", "teacher", "admin"], []),
        ("/submissions", [], "post",
            ["student"], ["student_other", "teacher", "admin"]),

        ("/submissions/@0", ["submission_id"], "get",
            ["student", "teacher", "admin"], ["student_other", "teacher_other", "admin_other"]),
        ("/submissions/@0", ["submission_id"], "patch",
            ["teacher", "admin"], ["student", "teacher_other", "admin_other"]),
    ])

    @mark.parametrize("auth_test", authentication, indirect=True)
    def test_authentication(self, auth_test: Tuple[str, any]):
        """Test the authentication"""
        super().authentication(auth_test)

    @mark.parametrize("auth_test", authorization, indirect=True)
    def test_authorization(self, auth_test: Tuple[str, any, str, bool]):
        """Test the authorization"""
        super().authorization(auth_test)



    ### GET SUBMISSIONS ###
    def test_get_submissions_wrong_user(self, client: FlaskClient):
        """Test getting submissions for a non-existing user"""
        response = client.get("/submissions?uid=no_user", headers = {"Authorization": "teacher"})
        assert response.status_code == 400

    def test_get_submissions_user(
            self, client: FlaskClient, api_host: str, student: User, submission: Submission
        ):
        """Test getting submission from a student"""
        response = client.get(
            f"/submissions?uid={student.uid}",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 200
        assert response.json["data"][0]["submission_id"] == \
            f"{api_host}/submissions/{submission.submission_id}"

    def test_get_submissions_wrong_project_type(self, client: FlaskClient):
        """Test getting submissions for a non-existing project of the wrong type"""
        response = client.get(
            "/submissions?project_id=no_project",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 400

    def test_get_submissions_wrong_project(self, client: FlaskClient):
        """Test getting submissions for a non-existing project"""
        response = client.get(
            "/submissions?project_id=0",
            headers = {"Authorization": "teacher"}
        )
        assert response.status_code == 400

    def test_get_submissions_project(
            self, client: FlaskClient, api_host: str, submission: Submission
        ):
        """Test getting the submissions given a specific project"""
        response = client.get("/submissions", headers = {"Authorization": "teacher"})
        assert response.status_code == 200
        assert response.json["data"][0]["submission_id"] == \
            f"{api_host}/submissions/{submission.submission_id}"



    ### POST SUBMISSIONS ###



    ### GET SUBMISSION ###
    def test_get_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test getting a submission for a non-existing submission id"""
        response = client.get("/submissions/0", headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 404
        assert data["message"] == "Submission with id: 0 not found"

    def test_get_submission_correct(self, client: FlaskClient, api_host: str, session: Session):
        """Test getting a submission"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student01", project_id=project.project_id
        ).first()
        response = client.get(f"/submissions/{submission.submission_id}",
                              headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 200
        assert data["message"] == "Successfully fetched the submission"
        assert data["data"] == {
            "id": f"{api_host}/submissions/{submission.submission_id}",
            "user": f"{api_host}/users/student01",
            "project": f"{api_host}/projects/{project.project_id}",
            "grading": 16,
            "time": "Thu, 14 Mar 2024 12:00:00 GMT",
            "status": 'SUCCESS'
        }

    ### PATCH SUBMISSION ###
    def test_patch_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test patching a submission for a non-existing submission id"""
        response = client.patch("/submissions/0", data={"grading": 20},
                                headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 404
        assert data["message"] == "Submission with id: 0 not found"

    def test_patch_submission_wrong_grading(self, client: FlaskClient, session: Session):
        """Test patching a submission with a wrong grading"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student02", project_id=project.project_id
        ).first()
        response = client.patch(f"/submissions/{submission.submission_id}",
                                data={"grading": 100},
                                headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid grading (grading=0-20)"

    def test_patch_submission_wrong_grading_type(self, client: FlaskClient, session: Session):
        """Test patching a submission with a wrong grading type"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student02", project_id=project.project_id
        ).first()
        response = client.patch(f"/submissions/{submission.submission_id}",
                                data={"grading": "zero"},
                                headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 400
        assert data["message"] == "Invalid grading (not a valid float)"

    def test_patch_submission_correct_teacher(self, client: FlaskClient, api_host: str, session: Session):
        """Test patching a submission"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student02", project_id=project.project_id
        ).first()
        response = client.patch(f"/submissions/{submission.submission_id}",
                                data={"grading": 20},
                                headers={"Authorization":"ad3_teacher"})
        data = response.json
        assert response.status_code == 200
        assert data["message"] == f"Submission (submission_id={submission.submission_id}) patched"
        assert data["url"] == f"{api_host}/submissions/{submission.submission_id}"
        assert data["data"] == {
            "id": f"{api_host}/submissions/{submission.submission_id}",
            "user": f"{api_host}/users/student02",
            "project": f"{api_host}/projects/{project.project_id}",
            "grading": 20,
            "time": 'Thu, 14 Mar 2024 23:59:59 GMT',
            "status": 'FAIL'
        }

    ### DELETE SUBMISSION ###
    def test_delete_submission_wrong_id(self, client: FlaskClient, session: Session):
        """Test deleting a submission for a non-existing submission id"""
        response = client.delete("submissions/0", headers={"Authorization":"student01"})
        data = response.json
        assert response.status_code == 404
        assert data["message"] == "Submission with id: 0 not found"

    def test_delete_submission_correct(self, client: FlaskClient, session: Session):
        """Test deleting a submission"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        submission = session.query(Submission).filter_by(
            uid="student01", project_id=project.project_id
        ).first()
        response = client.delete(f"submissions/{submission.submission_id}",
                                 headers={"Authorization":"student01"})
        data = response.json
        assert response.status_code == 200
        assert data["message"] == "Resource deleted successfully"
        assert submission.submission_id not in list(map(
            lambda s: s.submission_id, session.query(Submission).all()
        ))
