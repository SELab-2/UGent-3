"""Test the submissions API endpoint"""

from os import getenv
from typing import Any

from pytest import mark
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from project.models.project import Project
from project.models.submission import Submission
from tests.utils.auth_login import get_csrf_from_login
from tests.endpoints.endpoint import (
    TestEndpoint,
    authentication_tests,
    authorization_tests,
    data_field_type_tests,
    query_parameter_tests
)

API_HOST = getenv("API_HOST")

class TestSubmissionsEndpoint(TestEndpoint):
    """Class to test the submissions API endpoint"""

    ### AUTHENTICATION ###
    # Where is login required
    authentication_tests = \
        authentication_tests("/submissions", ["get", "post"]) + \
        authentication_tests("/submissions/@submission_id", ["get", "patch"]) + \
        authentication_tests("/submissions/@submission_id/download", ["get"])

    @mark.parametrize("auth_test", authentication_tests, indirect=True)
    def test_authentication(self, auth_test: tuple[str, Any, str, bool, dict[str, Any]]):
        """Test the authentication"""
        super().authentication(auth_test)



    ### AUTHORIZATION ###
    # Who can access what
    authorization_tests = \
        authorization_tests("/submissions", "get",
            ["student", "student_other", "teacher", "teacher_other", "admin", "admin_other"],
            []) + \
        authorization_tests("/submissions", "post",
            ["student"],
            ["student_other", "teacher", "teacher_other", "admin", "admin_other"]) + \
        authorization_tests("/submissions/@submission_id", "get",
            ["student", "teacher", "admin"],
            ["student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("submissions/@submission_id", "patch",
            ["teacher", "admin"],
            ["student", "student_other", "teacher_other", "admin_other"]) + \
        authorization_tests("submissions/@submission_id/download", "get",
            ["student", "teacher", "admin"],
            ["student_other", "teacher_other", "admin_other"])

    @mark.parametrize("auth_test", authorization_tests, indirect=True)
    def test_authorization(self, auth_test: tuple[str, Any, str, bool, dict[str, Any]]):
        """Test the authorization"""
        super().authorization(auth_test)

    # ### GET SUBMISSIONS ###
    # def test_get_submissions_wrong_user(self, client: FlaskClient):
    #     """Test getting submissions for a non-existing user"""
    #     csrf = get_csrf_from_login(client, "teacher")
    #     response = client.get("/submissions?uid=-20", headers = {"X-CSRF-TOKEN":csrf})
    #     assert response.status_code == 400

    # def test_get_submissions_wrong_project(self, client: FlaskClient):
    #     """Test getting submissions for a non-existing project"""
    #     csrf = get_csrf_from_login(client, "teacher")
    #     response = client.get("/submissions?project_id=123456789",
    #                           headers = {"X-CSRF-TOKEN":csrf})
    #     assert response.status_code == 400
    #     assert "message" in response.json

    # def test_get_submissions_wrong_project_type(self, client: FlaskClient):
    #     """Test getting submissions for a non-existing project of the wrong type"""
    #     csrf = get_csrf_from_login(client, "teacher")
    #     response = client.get("/submissions?project_id=zero", headers = {"X-CSRF-TOKEN":csrf})
    #     assert response.status_code == 400
    #     assert "message" in response.json

    # def test_get_submissions_project(self, client: FlaskClient, valid_submission_entry):
    #     """Test getting the submissions given a specific project"""
    #     csrf = get_csrf_from_login(client, "teacher")
    #     response = client.get(f"/submissions?project_id={valid_submission_entry.project_id}",
    #                           headers = {"X-CSRF-TOKEN":csrf})
    #     data = response.json
    #     assert response.status_code == 200
    #     assert "message" in data


    # ### GET SUBMISSION ###
    # def test_get_submission_wrong_id(self, client: FlaskClient, session: Session):
    #     """Test getting a submission for a non-existing submission id"""
    #     csrf = get_csrf_from_login(client, "ad3_teacher")
    #     response = client.get("/submissions/0", headers = {"X-CSRF-TOKEN":csrf})
    #     data = response.json
    #     assert response.status_code == 404
    #     assert data["message"] == "Submission with id: 0 not found"

    # def test_get_submission_correct(self, client: FlaskClient, session: Session):
    #     """Test getting a submission"""
    #     project = session.query(Project).filter_by(title="B+ Trees").first()
    #     submission = session.query(Submission).filter_by(
    #         uid="student01", project_id=project.project_id
    #     ).first()
    #     csrf = get_csrf_from_login(client, "ad3_teacher")
    #     response = client.get(f"/submissions/{submission.submission_id}",
    #                           headers = {"X-CSRF-TOKEN":csrf})
    #     data = response.json
    #     assert response.status_code == 200
    #     assert data["message"] == "Successfully fetched the submission"
    #     assert data["data"] == {
    #         "submission_id": f"{API_HOST}/submissions/{submission.submission_id}",
    #         "uid": f"{API_HOST}/users/student01",
    #         "project_id": f"{API_HOST}/projects/{project.project_id}",
    #         "grading": 16,
    #         "submission_time": "Thu, 14 Mar 2024 12:00:00 GMT",
    #         "submission_status": 'SUCCESS'
    #     }

    # ### PATCH SUBMISSION ###
    # def test_patch_submission_wrong_id(self, client: FlaskClient, session: Session):
    #     """Test patching a submission for a non-existing submission id"""
    #     csrf = get_csrf_from_login(client, "ad3_teacher")
    #     response = client.patch("/submissions/0", data={"grading": 20},
    #                             headers = {"X-CSRF-TOKEN":csrf})
    #     data = response.json
    #     assert response.status_code == 404
    #     assert data["message"] == "Submission with id: 0 not found"

    # def test_patch_submission_wrong_grading(self, client: FlaskClient, session: Session):
    #     """Test patching a submission with a wrong grading"""
    #     project = session.query(Project).filter_by(title="B+ Trees").first()
    #     submission = session.query(Submission).filter_by(
    #         uid="student02", project_id=project.project_id
    #     ).first()
    #     csrf = get_csrf_from_login(client, "ad3_teacher")
    #     response = client.patch(f"/submissions/{submission.submission_id}",
    #                             data={"grading": 100},
    #                             headers = {"X-CSRF-TOKEN":csrf})
    #     data = response.json
    #     assert response.status_code == 400
    #     assert data["message"] == "Invalid grading (grading=0-20)"

    # def test_patch_submission_wrong_grading_type(self, client: FlaskClient, session: Session):
    #     """Test patching a submission with a wrong grading type"""
    #     project = session.query(Project).filter_by(title="B+ Trees").first()
    #     submission = session.query(Submission).filter_by(
    #         uid="student02", project_id=project.project_id
    #     ).first()
    #     csrf = get_csrf_from_login(client, "ad3_teacher")
    #     response = client.patch(f"/submissions/{submission.submission_id}",
    #                             data={"grading": "zero"},
    #                             headers = {"X-CSRF-TOKEN":csrf})
    #     data = response.json
    #     assert response.status_code == 400
    #     assert data["message"] == "Invalid grading (not a valid float)"

    # def test_patch_submission_correct_teacher(self, client: FlaskClient, session: Session):
    #     """Test patching a submission"""
    #     project = session.query(Project).filter_by(title="B+ Trees").first()
    #     submission = session.query(Submission).filter_by(
    #         uid="student02", project_id=project.project_id
    #     ).first()
    #     csrf = get_csrf_from_login(client, "ad3_teacher")
    #     response = client.patch(f"/submissions/{submission.submission_id}",
    #                             data={"grading": 20},
    #                             headers = {"X-CSRF-TOKEN":csrf})
    #     data = response.json
    #     assert response.status_code == 200
    #     assert data["message"] == f"Submission (submission_id={submission.submission_id}) patched"
    #     assert data["url"] == f"{API_HOST}/submissions/{submission.submission_id}"
    #     assert data["data"] == {
    #         "id": f"{API_HOST}/submissions/{submission.submission_id}",
    #         "user": f"{API_HOST}/users/student02",
    #         "project": f"{API_HOST}/projects/{project.project_id}",
    #         "grading": 20,
    #         "time": 'Thu, 14 Mar 2024 23:59:59 GMT',
    #         "status": 'FAIL'
    #     }
